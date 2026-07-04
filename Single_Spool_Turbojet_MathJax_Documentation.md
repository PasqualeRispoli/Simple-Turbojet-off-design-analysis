# Technical Documentation: Single Spool Turbojet Simulation Model

This document provides a rigorous, comprehensive, and error-free technical reference for the thermodynamic simulation model of a single-spool turbojet engine. It details the Python software architecture, underlying physical principles, governing equations for both **Design Point (DP)** and **Off-Design (OD)** conditions, component map scaling methodology, and the multidimensional numerical convergence solver based on the Newton-Raphson method. 

---

## 1. Software Architecture and Modularity

The simulator is built with a modular, object-oriented structure across three interdependent Python scripts:

```
├── MAIN_SP.py            # Main script: resolves cycle thermodynamics, DP matching, and the OD solver loop.
├── Compressor_map.py     # Compressor module: stores raw map data, applies scaling, and performs Pchip splines.
└── Turbine_map.py        # Turbine module: stores raw map data, applies scaling, and performs Pchip splines.
```

### Engine Thermodynamic Stations
The flow path follows the standard gas turbine station numbering convention:
* **Station 0**: Ambient/Freestream conditions (static flight environment).
* **Station 1**: Compressor Inlet (stagnation properties after the intake duct).
* **Station 2**: Compressor Discharge / Combustor Inlet.
* **Station 3**: Combustor Discharge / Turbine Inlet.
* **Station 4**: Turbine Discharge / Exhaust Nozzle Inlet.
* **Station 5**: Nozzle Exit Plane (choked or expanded static state).

---

## 2. Gas Properties and Global Constants

To achieve high physical fidelity, the model accounts for the variations in specific heat and molecular composition between the clean air compression phase and the post-combustion gas expansion phase:

| Variable | Symbol | Value | Unit | Application Domain |
| :--- | :--- | :--- | :--- | :--- |
| `T_ref` | $T_{\text{ref}}$ | $273.0$ | $\text{K}$ | Standard reference temperature for corrected parameters |
| `p_ref` | $p_{\text{ref}}$ | $101315.0$ | $\text{Pa}$ | Standard reference pressure for corrected parameters |
| `cp` | $c_p$ | $1004.0$ | $\text{J}/(\text{kg}\cdot\text{K})$ | Specific heat at constant pressure - Air (Stations 0 to 2) |
| `cp_gc` | $c_{p,\text{gc}}$ | $1184.0$ | $\text{J}/(\text{kg}\cdot\text{K})$ | Specific heat at constant pressure - Gas Burned (Stations 3 to 5) |
| `gamma` | $\gamma$ | $1.40$ | $-$ | Ratio of specific heats - Air (Stations 0 to 2) |
| `gamma_gc` | $\gamma_{\text{gc}}$ | $1.33$ | $-$ | Ratio of specific heats - Gas Burned (Stations 3 to 5) |
| `R` | $R$ | $287.0$ | $\text{J}/(\text{kg}\cdot\text{K})$ | Gas constant for air |
| `R_gc` | $R_{\text{gc}}$ | $293.0$ | $\text{J}/(\text{kg}\cdot\text{K})$ | Gas constant for combustion products |
| `Q_f` | $Q_f$ | $43260000.0$ | $\text{J}/\text{kg}$ | Lower heating value of aviation fuel (Jet-A) |

---

## 3. Design Point (DP) Modeling

During Design Point synthesis, geometric restrictions are absent, and engine parameters are derived from targeted nominal cycle selections. The `DesignPoint()` function solves the thermodynamic cycle analytically.

### Flight Conditions and Intake
Given the flight Mach number $M_0$, ambient static pressure $p_0$, and ambient static temperature $T_0$, the stagnation conditions at the compressor face (Station 1) are derived assuming an ideal ram recovery process (isobaric intake, $\pi_{\text{IN}} = 1$):
$$a_0 = \sqrt{\gamma R T_0}$$
$$V_0 = M_0 \cdot a_0$$
$$T_{0,0} = T_{1,0} = T_0 \left( 1 + \frac{\gamma - 1}{2} M_0^2 \right)$$
$$p_{0,0} = p_{1,0} = p_0 \left( 1 + \frac{\gamma - 1}{2} M_0^2 \right)^{\frac{\gamma}{\gamma - 1}}$$

### Compression System
With the design pressure ratio $\pi_C$ and compressor isentropic efficiency $\eta_C$ specified, the stagnation state at Station 2 is determined by:
$$p_{2,0} = \pi_C \cdot p_{1,0}$$

$$\tau_C = 1 + \frac{1}{\eta_C} \left( \pi_C^{\frac{\gamma - 1}{\gamma}} - 1 \right)$$

$$T_{2,0} = \tau_C \cdot T_{1,0}$$

### Combustion Chamber (CC)
Given the fuel-to-air ratio $f = \frac{\dot{m}_f}{\dot{m}_a}$, the combustor is modeled as ideal without total pressure losses ($\pi_B = 1$). The turbine inlet total temperature $T_{3,0}$ is found directly from the enthalpy energy balance:
$$p_{3,0} = p_{2,0}$$

$$\dot{m}_a c_p T_{2,0} + \dot{m}_f Q_f = (\dot{m}_a + \dot{m}_f) c_{p,\text{gc}} T_{3,0} \implies T_{3,0} = \frac{f Q_f + c_p T_{2,0}}{(1 + f) c_{p,\text{gc}}}$$

The burner temperature ratio is designated as $\tau_B = \frac{T_{3,0}}{T_{2,0}}$.

### Expansion Turbine
In a single-spool configuration, the mechanical power extracted by the turbine must balance the power required by the compressor, assuming a purely rigid shaft coupling with a mechanical efficiency of unity:

$$\mathcal{P}_C = \mathcal{P}_T \implies \dot{m}_a c_p (T_{2,0} - T_{1,0}) = (\dot{m}_a + \dot{m}_f) c_{p,\text{gc}} (T_{3,0} - T_{4,0})$$

Rearranging the balance terms yields the non-dimensional turbine temperature drop ratio $\tau_T = \frac{T_{4,0}}{T_{3,0}}$:

$$\tau_T = 1 - \frac{c_p}{c_{p,\text{gc}} \cdot \tau_B \cdot (1 + f)} \left( 1 - \frac{1}{\tau_C} \right)$$

$$T_{4,0} = \tau_T \cdot T_{3,0}$$

Utilizing the design-point turbine adiabatic efficiency $\eta_T$, the corresponding expansion pressure ratio $\pi_T = \frac{p_{4,0}}{p_{3,0}}$ is computed:

$$\pi_T = \left[ 1 - \frac{1}{\eta_T} (1 - \tau_T) \right]^{\frac{\gamma_{\text{gc}}}{\gamma_{\text{gc}} - 1}}$$

$$p_{4,0} = \pi_T \cdot p_{3,0}$$

### Exhaust Nozzle and Geometric Sizing
The convergent nozzle expands the combustion gases back to the atmospheric pressure $p_0$. The code evaluates the occurrence of acoustic choking ($M_5 = 1$) by evaluating the critical pressure expansion ratio $\beta_{\text{cr}}$:

$$\beta_{\text{cr}} = \left( \frac{\gamma_{\text{gc}} + 1}{2} \right)^{-\frac{\gamma_{\text{gc}}}{\gamma_{\text{gc}} - 1}}$$

* **Condition 1: Choked Nozzle** if $\frac{p_0}{p_{4,0}} > \beta_{\text{cr}}$:
  $$M_5 = 1.0$$
  
  $$p_5 = \frac{p_{4,0}}{\beta_{\text{cr}}}$$
  
  $$T_5 = T_{4,0} \left( \frac{\gamma_{\text{gc}} + 1}{2} \right)^{-1}$$

* **Condition 2: Unchoked Nozzle** if $\frac{p_0}{p_{4,0}} \le \beta_{\text{cr}}$:
  $$p_5 = p_0$$
  
  $$M_5 = \sqrt{ \left[ \left( \frac{p_{4,0}}{p_0} \right)^{\frac{\gamma_{\text{gc}} - 1}{\gamma_{\text{gc}}}} - 1 \right] \frac{2}{\gamma_{\text{gc}} - 1} }$$
  
  $$T_5 = \frac{T_{4,0}}{1 + \frac{\gamma_{\text{gc}}-1}{2} M_5^2}$$

The physical exit velocity $V_5$, static density $\rho_5$, and the fixed geometric nozzle area $A_5$ (which forms an unalterable constraint in subsequent Off-Design operations) are defined by:
$$V_5 = M_5 \sqrt{\gamma_{\text{gc}} R_{\text{gc}} T_5}, \quad \rho_5 = \frac{p_5}{R_{\text{gc}} T_5}$$

$$A_5 = \frac{\dot{m}_a (1 + f)}{\rho_5 V_5}$$

Net thrust output $F_{\text{thrust}}$ and Thrust Specific Fuel Consumption ($TSFC$) are evaluated as:

$$F_{\text{thrust}} = \dot{m}_a \left[ (1 + f) V_5 - V_0 \right] + A_5 (p_5 - p_0)$$

$$TSFC = \frac{\dot{m}_f}{F_{\text{thrust}}}$$

---

## 4. Component Map Mathematics and Scaling

In Off-Design match routines, the physical boundaries are frozen ($A_5 = \text{const}$), and component responses are extracted from experimental digitized maps. These maps operate using corrected, dimensionless variables that must be normalized against the Design Point values.

### Corrected Map Parameters
Mass flow rates and rotational spool speeds are corrected to eliminate the variations caused by inlet total temperature and pressure fluctuations:

$$\dot{m}_{\text{corr}} = \dot{m} \frac{\sqrt{T_{\text{in},0}/T_{\text{ref}}}}{p_{\text{in},0}/p_{\text{ref}}}, \quad N_{\text{corr}} = \frac{N}{\sqrt{T_{\text{in},0}/T_{\text{ref}}}}$$

### Scaling Factors
To map generic or commercial performance charts directly onto the calculated cycle's design point, linear scaling factors are established at the reference line. Every label is strictly protected within MathJax standard text blocks:

* **Compressor Scaling Factors:**
  $$f_{m,C} = \frac{\dot{m}_{C,\text{dp}}}{\dot{m}_{C,\text{unscaled,dp}}}$$
  
  $$f_{\text{PR},C} = \frac{\pi_{C,\text{dp}} - 1}{\pi_{C,\text{unscaled,dp}} - 1}$$
  
  $$f_{\eta,C} = \frac{\eta_{C,\text{dp}}}{\eta_{C,\text{unscaled,dp}}}$$

* **Turbine Scaling Factors:**
  $$f_{m,T} = \frac{\dot{m}_{T,\text{dp}}}{\dot{m}_{T,\text{unscaled,dp}}}$$
  
  $$f_{\text{PR},T} = \frac{(1/\pi_{T,\text{dp}}) - 1}{\pi_{T,\text{unscaled,dp}} - 1}$$
  
  $$f_{\eta,T} = \frac{\eta_{T,\text{dp}}}{\eta_{T,\text{unscaled,dp}}}$$

### Monotonic Interpolation Algorithm
Data fetching inside `Compressor_map.py` and `Turbine_map.py` utilizes an advanced two-step procedure:
1. **Speedline Boundary Location:** The script isolates the two nominal constant speedlines ($N_{\text{corr}}$) bounding the requested operational target speed.
2. **Monotonic Spline Reconstruction:** A weighted intermediate curve is computed linearly based on percentage positioning. On this curve, a `PchipInterpolator` (`Piecewise Cubic Hermite Interpolating Polynomial`) from `scipy` is evaluated. Choosing `Pchip` is vital compared to traditional standard cubic splines because it **strictly preserves data monotonicity**, preventing numerical overshoot (*Runge's phenomenon*) that typically compromises solver convergence.

---

## 5. Off-Design Matching Framework

During Off-Design excursions, the environmental state ($M_0, p_0, T_0$) is predefined, the nozzle area $A_5$ remains constant, and engine throttling is dictated by the user via the input parameter:

$$\tau_{\text{th}} = \frac{T_{3,0}}{T_{1,0}}$$

### State Variable Vector ($X$)
The non-linear engine component tracking loop contains 3 independent degrees of freedom, gathered into the state matrix $X \in \mathbb{R}^3$:

$$X = \begin{bmatrix} \dot{m}_{C,\text{corr}} \\ N_{C,\text{perc}} \\ \pi_T \end{bmatrix}$$

1. $\dot{m}_{C,\text{corr}}$: Corrected mass flow rate entering the compressor face.
2. $N_{C,\text{perc}}$: Percentage/corrected rotational speed of the compressor spool.
3. $\pi_T$: Total expansion pressure ratio across the turbine stage ($p_{4,0}/p_{3,0}$).

### Error Residual Equations ( $F(X)$ )

A physically consistent steady-state operating condition is established if and only if all three residual error functions in vector $F(X) = [f_1, f_2, f_3]^T$ converge identically to zero:

1. **Turbine Mass Flow Continuity Error ($f_1$):**
   The true physical mass flow transiting the turbine from cycle properties must match the corrected mass flow predicted by the scaled turbine performance chart:
   
   $$\dot{m}_{T,\text{cycle}} = \dot{m}_{a,\text{OD}} \cdot (1 + f)$$
   
   $$\dot{m}_{T,\text{map}} = \text{Turbine.Interpolate}\left(N_{T,\text{corr}}, \pi_T\right) \cdot \frac{p_{3,0}/p_{\text{ref}}}{\sqrt{T_{3,0}/T_{\text{ref}}}}$$
   
   $$f_1 = \frac{\dot{m}_{T,\text{map}} - \dot{m}_{T,\text{cycle}}}{\dot{m}_{T,\text{dp}}} = 0$$

3. **Nozzle Area Geometric Compatibility Error ($f_2$):**
   The exhaust area required to expand the operational gas volume under current Off-Design constraints ($A_{5,\text{OD}}$) must match the unalterable physical throat dimension established during cycle design ($A_{5,\text{dp}}$):
   
   $$f_2 = \frac{A_{5,\text{dp}} - A_{5,\text{OD}}}{A_{5,\text{dp}}} = 0$$

5. **Spool Power Balance Error ($f_3$):**
   For steady state operation (omitting transient engine acceleration or deceleration terms), the mechanical power absorbed by the compression stage must be exactly equal to the gas expansion power output by the turbine stage:
   
   $$\mathcal{P}_{C,\text{OD}} = \dot{m}_{a,\text{OD}} \cdot c_p \cdot (T_{2,0,\text{OD}} - T_{1,0,\text{OD}})$$
   
   $$\mathcal{P}_{T,\text{OD}} = \dot{m}_{a,\text{OD}} \cdot (1 + f) \cdot c_{p,\text{gc}} \cdot (T_{3,0,\text{OD}} - T_{4,0,\text{OD}})$$
   
   $$f_3 = \frac{\mathcal{P}_{C,\text{OD}}}{\mathcal{P}_{T,\text{OD}}} - 1 = 0$$

---

## 6. Newton-Raphson Multidimensional Numerical Solver

The complex non-linear system $F(X) = 0$ is iteratively solved inside `MAIN_SP.py` via a quasi-analytical multi-variable Newton-Raphson numerical scheme.

### State Vector Correction Step
Starting from a given iteration step $k$, the subsequent approximation $X^{(k+1)}$ is formulated by solving the linear set against the local Jacobian matrix $J \in \mathbb{R}^{3 \times 3}$:

$$X^{(k+1)} = X^{(k)} - [J(X^{(k)})]^{-1} F(X^{(k)})$$

### Forward-Difference Jacobian Approximation
Because map boundaries lack continuous analytical derivatives, the local gradient space is mapped numerically by introducing an infinitesimal forward perturbation step $\epsilon = 10^{-13}$ sequentially to each individual state variable:

$$\Delta X_j = \epsilon \cdot X_j$$

Each element of the Jacobian matrix $J_{i,j}$ is filled using the finite difference ratio:

$$J_{i,j} = \frac{\partial f_i}{\partial X_j} \approx \frac{f_i(X_0, \dots, X_j + \Delta X_j, \dots, X_n) - f_i(X_0, \dots, X_j, \dots, X_n)}{\Delta X_j}$$

The resulting structural topology of the system matrix is defined as:

$$J = \begin{bmatrix} 
\frac{\partial f_1}{\partial \dot{m}_{C,\text{corr}}} & \frac{\partial f_1}{\partial N_{C,\text{perc}}} & \frac{\partial f_1}{\partial \pi_T} \\ 
\frac{\partial f_2}{\partial \dot{m}_{C,\text{corr}}} & \frac{\partial f_2}{\partial N_{C,\text{perc}}} & \frac{\partial f_2}{\partial \pi_T} \\ 
\frac{\partial f_3}{\partial \dot{m}_{C,\text{corr}}} & \frac{\partial f_3}{\partial N_{C,\text{perc}}} & \frac{\partial f_3}{\partial \pi_T}
\end{bmatrix}$$

Matrix inversion and correction steps are computed efficiently via `scipy.linalg.solve()`, ensuring high stability and preventing numerical accumulation errors. The iteration loop terminates cleanly once the standard $L_2$ error norm meets a stringent absolute tolerance:
$$\|F(X)\|_2 < 10^{-14}$$

---

## 7. Output Structures and Graphical Visualization

Post-execution, the core routine transforms the array records into easily readable structures and triggers an advanced post-processing visualization:
1. **`DP_param` and `OD_param`**: Structured Python dictionaries collecting every thermodynamic metric ($p, T, M, V$) at each internal engine station, alongside geometric data, thrust metrics, and global cycle thermal efficiencies.
2. **Graphical Post-Processing**: Leveraging `matplotlib`, the system projects the entire scaled compressor performance envelope, tracing constant speedlines and explicitly marking both the **Design Point (DP)** and the solved **Off-Design (OD)** operating point. This provides engineers with immediate visual confirmation of the engine operating line and its safe distance from compressor surge/stall limits.
