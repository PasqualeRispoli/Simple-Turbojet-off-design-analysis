# Simple Turbojet Off-Design Analysis

A Python-based simulation tool for analyzing single-spool turbojet performance at both design point and off-design operating conditions. This code implements thermodynamic analysis of turbojet components and map-based off-design solution methods.

## Overview

This project performs detailed thermodynamic analysis of a turbojet engine consisting of:
- **Inlet**: Compresses incoming air at flight conditions
- **Compressor**: Increases air pressure and temperature
- **Combustor (CC)**: Burns fuel to heat the air
- **Turbine**: Expands hot gases to drive the compressor
- **Nozzle**: Accelerates exhaust gases for thrust generation

The analysis includes both:
1. **Design Point (DP)**: Reference operating condition where all parameters are specified
2. **Off-Design (OD)**: Arbitrary operating conditions solved using Newton-Raphson iteration

## Design Point Analysis

### Input Parameters

```
# Input parameters (Python-friendly names)
M_0   = 0.7              # Mach number at inlet
p_0   = 41059            # Pa (static pressure at sea level)
T_0   = 242              # K (static temperature at sea level)
mdot_a = 20.0            # kg/s (air mass flow rate)
pi_C  = 8.3              # Compressor pressure ratio
eta_C = 0.822            # Compressor isentropic efficiency
eta_T = 0.88             # Turbine isentropic efficiency
f     = 0.02             # Fuel-to-air ratio
Q_f   = 43.26e6          # J/kg (fuel lower heating value = 43.26 MJ/kg)
```

### Thermodynamic Properties

| Property | Value | Unit |
|----------|-------|------|
| γ (air) | 1.4 | - |
| γ_gc (hot gas) | 1.33 | - |
| R (air) | 287 | J/(kg·K) |
| R_gc (hot gas) | 293 | J/(kg·K) |
| c_p (air) | 1004 | J/(kg·K) |
| c_{p,\text{gc}} (hot gas) | 1184 | J/(kg·K) |
| T_ref | 273 | K |
| p_ref | 101315 | Pa |

### Stage 0: Inlet (Ramjet Effect)

Incoming air is compressed to stagnation conditions:

**Sound speed:**
$$a_0 = \sqrt{\gamma R T_0}$$

**Velocity:**
$$V_0 = M_0 \cdot a_0$$

**Stagnation pressure:**
$$p_{0,0} = p_0 \left(1 + \frac{\gamma-1}{2} M_0^2\right)^{\frac{\gamma}{\gamma-1}}$$

**Stagnation temperature:**
$$T_{0,0} = T_0 \left(1 + \frac{\gamma-1}{2} M_0^2\right)$$

**Inlet air density:**
$$\rho_0 = \frac{p_0}{R T_0}$$

**Inlet area:**
$$A_0 = \frac{\dot{m}_a}{\rho_0 V_0}$$

### Stage 1-2: Compressor

The compressor receives air at stagnation conditions and increases pressure with specified efficiency.

**Compressor temperature ratio:**
$$\tau_C = 1 + \frac{1}{\eta_C}\left(\pi_C^{\frac{\gamma-1}{\gamma}} - 1\right)$$

**Stagnation temperature at compressor exit:**
$$T_{2,0} = \tau_C \cdot T_{1,0}$$

**Stagnation pressure at compressor exit:**
$$p_{2,0} = \pi_C \cdot p_{1,0}$$

**Corrected mass flow (compressor):**
$$\dot{m}_{C,\mathrm{corr}} = \frac{\dot{m}_a \sqrt{\theta_1}}{\delta_1}$$

where:
- $\theta_1 = \dfrac{T_{1,0}}{T_{\mathrm{ref}}}$ (temperature ratio)
- $\delta_1 = \dfrac{p_{1,0}}{p_{\mathrm{ref}}}$ (pressure ratio)

### Stage 2-3: Combustor

Fuel is injected and burned at (approximately) constant pressure, heating the air.

**Stagnation pressure (constant):**
$$p_{3,0} = p_{2,0}$$

**Stagnation temperature (energy balance):**
$$T_{3,0} = \frac{f \cdot Q_f + c_p T_{2,0}}{(1+f) c_{p,\text{gc}}}$$

**Burner temperature ratio:**
$$\tau_B = \frac{T_{3,0}}{T_{2,0}}$$

**Burner pressure ratio:**
$$\pi_B = \frac{p_{3,0}}{p_{2,0}} = 1.0$$

**Corrected mass flow (turbine inlet):**
$$\dot{m}_{T,\mathrm{corr}} = \frac{\dot{m}_{\mathrm{gc}} \sqrt{\theta_3}}{\delta_3}$$

where $\dot{m}_{\mathrm{gc}} = (1+f) \dot{m}_a$ (gas flow rate)

### Stage 3-4: Turbine

The turbine extracts energy from hot gases to drive the compressor. Power balance constraint links turbine and compressor operation.

**Turbine temperature ratio:**
$$\tau_T = 1 - \frac{c_p}{c_{p,\text{gc}} \, \tau_B (1+f)} \left(1 - \frac{1}{\tau_C}\right)$$

**Turbine pressure ratio:**
$$\pi_T = \left[1 - \frac{1}{\eta_T}(1 - \tau_T)\right]^{\frac{\gamma_{\text{gc}}}{\gamma_{\text{gc}}-1}}$$

**Stagnation temperature at turbine exit:**
$$T_{4,0} = \tau_T \cdot T_{3,0}$$

**Stagnation pressure at turbine exit:**
$$p_{4,0} = \pi_T \cdot p_{3,0}$$

### Stage 4-5: Nozzle

Hot gases expand to ambient pressure through the convergent-divergent nozzle.

**Critical pressure ratio:**
$$\beta_{\text{cr}} = \left(\frac{\gamma_{\text{gc}}+1}{2}\right)^{-\frac{\gamma_{\text{gc}}}{\gamma_{\text{gc}}-1}}$$

**Nozzle expansion condition:**
- If $\beta > \beta_{\text{cr}}$ (subsonic exit):
  - Exit pressure: $p_5 = p_0$
  - Exit Mach: $M_5 = \sqrt{\left[\left(\frac{1}{\beta}\right)^{\frac{\gamma_{\text{gc}}-1}{\gamma_{\text{gc}}}} - 1\right] \frac{2}{\gamma_{\text{gc}}-1}}$

- If $\beta \leq \beta_{\text{cr}}$ (choked flow):
  - Exit pressure: $p_5 = \dfrac{p_{5,0}}{\beta_{\text{cr}}}$
  - Exit Mach: $M_5 = 1.0$

**Static temperature at nozzle exit:**
$$T_5 = \frac{T_{5,0}}{1 + \frac{\gamma_{\text{gc}}-1}{2} M_5^2}$$

**Sound speed and velocity:**
$$a_5 = \sqrt{\gamma_{\text{gc}} R_{\text{gc}} T_5}$$
$$V_5 = M_5 \cdot a_5$$

**Exit density and area:**
$$\rho_5 = \frac{p_5}{R_{\text{gc}} T_5}, \quad A_5 = \frac{\dot{m}_{\text{gc}}}{\rho_5 V_5}$$

### Performance Metrics

**Thrust (static):**
$$S = \dot{m}_a (1+f) V_5 - \dot{m}_a V_0 + A_5 (p_5 - p_0)$$

The first term is momentum thrust, the second is ram drag, and the third is pressure thrust.

**Compressor power extraction:**
$$P_{\text{ex}} = \dot{m}_a c_p (T_{2,0} - T_{1,0}) - \dot{m}_a (1+f) c_{p,\text{gc}} (T_{3,0} - T_{4,0})$$

## Component Maps

Component performance is characterized using two-dimensional maps:
- **Pressure Ratio (PR)** vs Corrected Mass Flow and Corrected Speed
- **Efficiency (η)** vs Corrected Mass Flow and Corrected Speed

### Compressor Map Scaling

The design point parameters scale the baseline compressor map:

**Scaling factors:**
$$f_m = \frac{\dot{m}_{C,\text{dp}}}{\dot{m}_{C,\text{udp}}}, \quad f_{\text{PR}} = \frac{\pi_{C,\text{dp}} - 1}{\pi_{C,\text{udp}} - 1}, \quad f_{\eta} = \frac{\eta_{C,\text{dp}}}{\eta_{C,\text{udp}}}$$

**Scaled map values:**
$$\dot{m}_{C,\text{scaled}} = f_m \cdot \dot{m}_{C,\text{ref}}$$
$$\pi_{C,\text{scaled}} = 1 + f_{\text{PR}} (\pi_{C,\text{ref}} - 1)$$
$$\eta_{C,\text{scaled}} = f_{\eta} \cdot \eta_{C,\text{ref}}$$

### Turbine Map Scaling

Similarly for the turbine with pressure ratio as the independent variable:

**Scaling factors:**
$$f_m = \frac{\dot{m}_{T,\text{dp}}}{\dot{m}_{T,\text{udp}}}, \quad f_{\text{PR}} = \frac{\pi_{T,\text{dp}} - 1}{\pi_{T,\text{udp}} - 1}, \quad f_{\eta} = \frac{\eta_{T,\text{dp}}}{\eta_{T,\text{udp}}}$$

**Scaled map values:**
$$\dot{m}_{T,\text{scaled}} = f_m \cdot \dot{m}_{T,\text{ref}}$$
$$\pi_{T,\text{scaled}} = 1 + f_{\text{PR}} (\pi_{T,\text{ref}} - 1)$$
$$\eta_{T,\text{scaled}} = f_{\eta} \cdot \eta_{T,\text{ref}}$$

### Map Interpolation

For a given corrected speed N and operating point x, the map is interpolated using:

1. **Speed band interpolation**: Linear interpolation between two nearby speed lines
2. **Operating line interpolation**: Hermite cubic spline (PCHIP) interpolation along the speed band

This ensures smooth, monotonic behavior across the component map.

## Off-Design Analysis

At off-design conditions, the system operates at different throttle settings while maintaining mechanical coupling between compressor and turbine on the same spool.

### Throttle Parameter

The throttle fraction $\mathrm{th}$ scales the design point thermal ratio:

$$\tau_{\text{th,OD}} = \tau_{\text{th,DP}} \cdot \mathrm{th}$$

For the analysis: $\mathrm{th} = 0.85$ (85% throttle = 85% of design power)

### Off-Design Equations

Given compressor mass flow $\dot{m}_C$, compressor speed $N_C$, and turbine pressure ratio $\pi_T$, the off-design system is solved using three governing equations:

#### Equation 1: Turbine Speed Coupling (Energy Balance)
$$f_1 = \frac{\dot{m}_{T,\mathrm{corr}} - (1+f) \dot{m}_a \sqrt{\theta_3}/\delta_3}{\dot{m}_{T,\text{dp,corr}}}$$

The turbine mass flow is determined from the turbine map at the coupled speed:
$$N_T = N_C \sqrt{\frac{\tau_{\text{th,DP}}}{\tau_{\text{th,OD}}}}$$

This equation ensures the turbine operates at the correct speed for the specified throttle setting.

#### Equation 2: Nozzle Area Constraint
$$f_2 = \frac{A_{5,\text{DP}} - A_5}{A_{5,\text{DP}}}$$

At design point, the nozzle area is fixed. Off-design operation must satisfy this constraint or indicate the need for a variable-geometry nozzle.

#### Equation 3: Power Balance
$$f_3 = \frac{\dot{m}_a c_p (T_{2,0} - T_{1,0})}{\dot{m}_a (1+f) c_{p,\text{gc}} (T_{3,0} - T_{4,0})} - 1$$

The compressor power input must equal the turbine power output (neglecting mechanical losses).

### Solution Method: Newton-Raphson

The three equations are solved using Newton-Raphson iteration:

**Jacobian matrix computation** (numerical differentiation):
$$J_{ij} = \frac{\partial f_i}{\partial X_j} \approx \frac{f_i(X_j + \epsilon X_j) - f_i(X_j)}{\epsilon X_j}$$

**Iteration:**
$$\mathbf{X}^{(k+1)} = \mathbf{X}^{(k)} - J^{-1}(\mathbf{X}^{(k)}) \mathbf{F}(\mathbf{X}^{(k)})$$

**Convergence criterion** (normalized residual):
$$\text{RES} = \frac{\|\mathbf{R}\|^{(k)} - \|\mathbf{R}\|^{(k-1)}}{\|\mathbf{R}\|^{(k-1)}} < 10^{-14}$$

where $\mathbf{R}$ is the vector of residuals normalized by design-point values.

## Code Structure

### Main Module: `MAIN_SP.py`

- **`DesignPoint()`**: Computes all design point parameters and returns dictionary of results
- **`Off_Design(DP, OD, m_C, N_C, pi_T)`**: Evaluates off-design equations for Newton-Raphson iteration
- **`Jacobian(X_0)`**: Computes numerical Jacobian matrix via finite differences
- **`F(X)`**: Evaluates residual vector
- **Newton-Raphson loop**: Iterates to convergence with maximum 100 iterations

### Component Modules

#### `Compressor_map.py`

```python
class Compressor:
    def scale_map(self, m_dp, PR_dp, eta_dp):
        # Scale design point to component map
    
    def map_interpolator(self, map_type, scaled, N, x):
        # Interpolate PR or efficiency at (N, x)
    
    def dispmap(self, map_type, scaled, x=0, y=0):
        # Display component map with operating points
```

#### `Turbine_map.py`

```python
class Turbine:
    def scale_map(self, m_dp, PR_dp, eta_dp):
        # Scale design point to component map
    
    def map_interpolator(self, map_type, scaled, N, x):
        # Interpolate PR or efficiency at (N, x)
    
    def dispmap(self, map_type, scaled, x=np.nan, y=np.nan):
        # Display component map with operating points
```

## Running the Code

1. **Initialize components** with baseline maps:
   ```python
   C = Compressor()
   T = Turbine()
   ```

2. **Calculate design point**:
   ```python
   DP = DesignPoint()
   ```

3. **Scale component maps** to design point:
   ```python
   C.scale_map(m_dp=m_C_dp, PR_dp=pi_C_dp, eta_dp=eta_C_dp)
   T.scale_map(m_dp=m_T_dp, PR_dp=1/pi_T_dp, eta_dp=eta_T_dp)
   ```

4. **Specify throttle setting**:
   ```python
   th = 0.85
   OD["tau_th"] = tau_th_dp * th
   ```

5. **Solve off-design point** via Newton-Raphson iteration (automated in code)

6. **Visualize results**:
   ```python
   C.dispmap(map_type="PR", scaled=True, x=[m_C_dp, m_C_od], y=[pi_C_dp, pi_C_od])
   plt.show()
   ```

## Key Physical Insights

1. **Compressor-Turbine Coupling**: The single spool constrains compressor and turbine to the same mechanical speed, creating an interdependent operating point.

2. **Throttle Effect**: Reducing thermal ratio $\tau_{\text{th}}$ via fuel flow reduces turbine power, which reduces compressor speed and mass flow, creating a new equilibrium.

3. **Map-Based Prediction**: Component maps capture realistic performance variations including efficiency islands and stall margins not captured by simple polytropic analysis.

4. **Nozzle Constraint**: Fixed nozzle area at design point limits off-design operation. Choked flow occurs when pressure ratio exceeds critical value.

5. **Speed Relationships**: Turbine speed adjusts inversely with thermal ratio to maintain mechanical balance—higher throttle requires higher speed.

## References

- **Thermodynamic Relations**: Standard turbomachinery thermodynamics following Cohen, Rogers & Saravanamuttoo conventions
- **Component Maps**: Normalized against realistic compressor and turbine characteristic maps
- **Off-Design Methods**: Based on component map interpolation and power-balance coupling typical in gas turbine performance analysis
