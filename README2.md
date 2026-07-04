# Single-Spool Turbojet Engine Simulation

This repository features a 0D numerical simulation framework written in Python to model the steady-state performance of a **Single-Spool Turbojet Engine**.
The software calculates thermodynamic states and performance metrics for both the **Design Point (DP)** and **Off-Design (OD)** operating conditions[cite: 6]. It matches real scaled component maps for the compressor and turbine through a multidimensional non-linear Newton-Raphson iterative solver[cite: 6].

---

## 📌 Engine Station Numbering
The thermodynamic cycle follows the classical aerospace engineering numbering convention to monitor stagnation properties[cite: 6]:
* **0**: Free-stream ambient conditions[cite: 6]
* **1**: Intake / Compressor Inlet[cite: 6]
* **2**: Compressor Discharge / Combustion Chamber Inlet[cite: 6]
* **3**: Combustion Chamber Discharge / Turbine Inlet Temperature (TIT)[cite: 6]
* **4**: Turbine Discharge / Nozzle Inlet[cite: 6]
* **5**: Exhaust Nozzle Exit Plane[cite: 6]

---

## 🛠️ Theoretical Framework & Mathematical Formulation

### 1. Design Point (DP)
At the Design Point, structural constraints, component efficiencies, reference map inputs ($T_{ref}$, $p_{ref}$), and ambient parameters are established[cite: 6].

* **Inlet Stagnation Conditions (Station 0 to 1):**
  Ram pressure recovery is computed from the flight Mach number $M_0$[cite: 6]:
  $$\theta_0 = 1 + \frac{\gamma - 1}{2} M_0^2$$
  $$T_{00} = T_0 \cdot \theta_0, \quad p_{00} = p_0 \cdot \theta_0^{\frac{\gamma}{\gamma-1}}$$
  Assuming an ideal intake with zero pressure drop: $p_{10} = p_{00}$ and $T_{10} = T_{00}$[cite: 6].

* **Compressor (Station 1 -> 2):**
  Given the target pressure ratio $\pi_C$ and adiabatic efficiency $\eta_C$[cite: 6]:
  $$\tau_C = 1 + \frac{1}{\eta_C} \left( \pi_C^{\frac{\gamma-1}{\gamma}} - 1 \right)$$
  $$T_{20} = \tau_C \cdot T_{10}, \quad p_{20} = \pi_C \cdot p_{10}$$

* **Combustion Chamber / Burner (Station 2 -> 3):**
  The fuel-to-air ratio $f = \dot{m}_f / \dot{m}_a$ needed to achieve the target Turbine Inlet Temperature ($T_{30}$) is derived from the energy balance[cite: 6]:
  $$T_{30} = \frac{f \cdot Q_f + c_p T_{20}}{(1+f) c_{p,gc}}$$
  $$\tau_B = \frac{T_{30}}{T_{20}}, \quad p_{30} = p_{20}$$

* **Turbine (Station 3 -> 4):**
  Based on the rotor shaft power balance, the power extracted by the turbine must balance the power absorbed by the compressor ($\mathcal{P}_T = \mathcal{P}_C$)[cite: 6]:
  $$(1+f)c_{p,gc}(T_{30} - T_{40}) = c_p (T_{20} - T_{10})$$
  $$\tau_T = 1 - \frac{c_p}{c_{p,gc} \cdot \tau_B \cdot (1+f)} \left( 1 - \frac{1}{\tau_C} \right)$$
  The expansion pressure ratio $\pi_T$ is calculated using the turbine efficiency $\eta_T$[cite: 6]:
  $$\pi_T = \left( 1 - \frac{1}{\eta_T}(1 - \tau_T) \right)^{\frac{\gamma_{gc}}{\gamma_{gc}-1}}$$
  $$T_{40} = \tau_T \cdot T_{30}, \quad p_{40} = \pi_T \cdot p_{30}$$

* **Exhaust Nozzle (Station 4 -> 5) & Net Thrust:**
  The critical expansion nozzle ratio $\beta_{cr}$ separates subcritical from choked operations[cite: 6]:
  $$\beta = \frac{p_0}{p_{50}}, \quad \beta_{cr} = \left( \frac{\gamma_{gc} + 1}{2} \right)^{-\frac{\gamma_{gc}}{\gamma_{gc}-1}}$$
  * **Unchoked / Adapted Nozzle ($\beta > \beta_{cr}$):** $p_5 = p_0$, giving full expansion[cite: 6]. The exit Mach number is[cite: 6]:
    $$M_5 = \sqrt{\frac{2}{\gamma_{gc}-1} \left[ \left(\frac{1}{\beta}\right)^{\frac{\gamma_{gc}-1}{\gamma_{gc}}} - 1 \right]}$$
  * **Choked Nozzle ($\beta \le \beta_{cr}$):** The flow reaches sonic velocity at the throat ($M_5 = 1$), and the exit static pressure stays above ambient: $p_5 = \frac{p_{50}}{\beta_{cr}}$[cite: 6].

  Net thrust ($S$) and Thrust Specific Fuel Consumption (**TSFC**) are computed via[cite: 6]:
  $$S = \dot{m}_a \left[ (1+f)V_5 - V_0 \right] + A_5(p_5 - p_0)$$
  $$\text{TSFC} = \frac{\dot{m}_f}{S}$$

---

### 2. Off-Design Conditions & Component Matching
During Off-Design maneuvers, the throat/exit area of the nozzle ($A_{5,dp}$) remains fixed[cite: 6]. The engine operational state reacts to changes in throttle inputs, defined by the cycle temperature ratio $\tau_{th} = T_{30}/T_{10}$[cite: 6].

The matching solver finds the three-dimensional unknown state vector[cite: 6]:
$$X = \begin{bmatrix} \dot{m}_{C,corr} \\ N_{C,corr} \\ \pi_T \end{bmatrix}$$

This vector satisfies the zero-residual convergence condition $F(X) = 0$ for three non-linear physical matching equations[cite: 6]:
1. **Turbine Mass Flow Continuity ($f_1$):** Ensures the mass flow from the turbine map matches the physical flow coming from the combustion chamber[cite: 6].
   $$f_1 = \frac{\dot{m}_{T,map} - \frac{\dot{m}_{gc}\sqrt{\theta_3}}{\delta_3}}{\dot{m}_{T,dp}} = 0$$
2. **Nozzle Geometric Area Consistency ($f_2$):** Assures that the calculated exit area matches the physical hardware area $A_{5,dp}$[cite: 6].
   $$f_2 = \frac{A_{5,dp} - A_5(X)}{A_{5,dp}} = 0$$
3. **Rotor Shaft Power Equilibrium ($f_3$):** Guarantees steady-state power matching between the compressor and the turbine[cite: 6].
   $$f_3 = \frac{\dot{m}_a c_p (T_{20} - T_{10})}{\dot{m}_{gc} c_{p,gc} (T_{30} - T_{40})} - 1 = 0$$

---

### 3. Numerical Solver (Newton-Raphson Method)
The system is solved iteratively by building a numerical Jacobian matrix $J$ at each iteration step[cite: 6]:
$$J_{ij} = \frac{\partial F_i}{\partial X_j} \approx \frac{F_i(X + \epsilon X_j \cdot e_j) - F_i(X)}{\epsilon X_j}$$

The state vector updates via the multi-variable root-finding scheme[cite: 6]:
$$X^{k+1} = X^k - J^{-1} F(X^k)$$

A strict tracking tolerance of `1e-14` is enforced within `MAIN_SP.py` to ensure high convergence accuracy and physical conservation laws[cite: 6].

---

## 📂 Codebase Structure

* `Compressor_map.py`: Contains the `Compressor` class[cite: 6]. It ingests discrete experimental performance data, applies scaling transformations based on DP values, and builds continuous curves using Piecewise Cubic Hermite Interpolating Polynomials (`scipy.interpolate.PchipInterpolator`) to guarantee monotonicity[cite: 6].
* `Turbine_map.py`: Contains the `Turbine` class, modeling flow capacity and efficiency characteristics relative to the expansion ratio $\pi_T$[cite: 6].
* `MAIN_SP.py`: The central orchestration file[cite: 6]. It solves the analytical design point, scales the component maps, initializes the Off-Design matching problem, and executes the Newton-Raphson solver[cite: 6]. It also generates comparative performance plots[cite: 6].

---

## 🚀 Requirements & Quick Start

### Dependencies
Install the required scientific packages[cite: 6]:
```bash
pip install numpy scipy matplotlib pandas
