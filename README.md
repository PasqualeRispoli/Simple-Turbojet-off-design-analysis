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

```python
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
| c_{p,\mathrm{gc}} (hot gas) | 1184 | J/(kg·K) |
| T_ref | 273 | K |
| p_ref | 101315 | Pa |

---

## Stage 0: Inlet (Ramjet Effect)

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

---

## Stage 1-2: Compressor

**Compressor temperature ratio:**
$$\tau_C = 1 + \frac{1}{\eta_C}\left(\pi_C^{\frac{\gamma-1}{\gamma}} - 1\right)$$

**Stagnation temperature at compressor exit:**
$$T_{2,0} = \tau_C \cdot T_{1,0}$$

**Stagnation pressure at compressor exit:**
$$p_{2,0} = \pi_C \cdot p_{1,0}$$

**Corrected mass flow (compressor):**
$$\dot{m}_{C,\mathrm{corr}} = \frac{\dot{m}_a \sqrt{\theta_1}}{\delta_1}$$

where:
- $\theta_1 = \dfrac{T_{1,0}}{T_{\mathrm{ref}}}$
- $\delta_1 = \dfrac{p_{1,0}}{p_{\mathrm{ref}}}$

---

## Stage 2-3: Combustor

**Stagnation pressure:**
$$p_{3,0} = p_{2,0}$$

**Stagnation temperature:**
$$T_{3,0} = \frac{f Q_f + c_p T_{2,0}}{(1+f)c_{p,\mathrm{gc}}}$$

**Burner temperature ratio:**
$$\tau_B = \frac{T_{3,0}}{T_{2,0}}$$

**Burner pressure ratio:**
$$\pi_B = \frac{p_{3,0}}{p_{2,0}} = 1.0$$

**Corrected mass flow (turbine inlet):**
$$\dot{m}_{T,\mathrm{corr}} = \frac{\dot{m}_{\mathrm{gc}} \sqrt{\theta_3}}{\delta_3}$$

where $\dot{m}_{\mathrm{gc}} = (1+f)\dot{m}_a$

---

## Stage 3-4: Turbine

**Temperature ratio:**
$$\tau_T = 1 - \frac{c_p}{c_{p,\mathrm{gc}} \, \tau_B (1+f)} \left(1 - \frac{1}{\tau_C}\right)$$

**Pressure ratio:**
$$\pi_T = \left[1 - \frac{1}{\eta_T}(1 - \tau_T)\right]^{\frac{\gamma_{\mathrm{gc}}}{\gamma_{\mathrm{gc}}-1}}$$

**Exit conditions:**
$$T_{4,0} = \tau_T \cdot T_{3,0}, \quad p_{4,0} = \pi_T \cdot p_{3,0}$$

---

## Stage 4-5: Nozzle

**Critical pressure ratio:**
$$\beta_{\mathrm{cr}} = \left(\frac{\gamma_{\mathrm{gc}}+1}{2}\right)^{-\frac{\gamma_{\mathrm{gc}}}{\gamma_{\mathrm{gc}}-1}}$$

**Nozzle expansion condition:**

- If $\beta > \beta_{\mathrm{cr}}$:
  - $p_5 = p_0$
  - $M_5 = \sqrt{\left[\left(\frac{1}{\beta}\right)^{\frac{\gamma_{\mathrm{gc}}-1}{\gamma_{\mathrm{gc}}}} - 1\right] \frac{2}{\gamma_{\mathrm{gc}}-1}}$

- If $\beta \leq \beta_{\mathrm{cr}}$:
  - $p_5 = \dfrac{p_{5,0}}{\beta_{\mathrm{cr}}}$
  - $M_5 = 1.0$

---

## Exit Flow

$$T_5 = \frac{T_{5,0}}{1 + \frac{\gamma_{\mathrm{gc}}-1}{2} M_5^2}$$

$$a_5 = \sqrt{\gamma_{\mathrm{gc}} R_{\mathrm{gc}} T_5}$$

$$V_5 = M_5 a_5$$

$$\rho_5 = \frac{p_5}{R_{\mathrm{gc}} T_5}, \quad A_5 = \frac{\dot{m}_{\mathrm{gc}}}{\rho_5 V_5}$$

---

## Performance Metrics

**Thrust:**
$$S = \dot{m}_a (1+f)V_5 - \dot{m}_a V_0 + A_5 (p_5 - p_0)$$

**Compressor power extraction:**
$$P_{\mathrm{ex}} = \dot{m}_a c_p (T_{2,0} - T_{1,0}) - \dot{m}_a (1+f) c_{p,\mathrm{gc}} (T_{3,0} - T_{4,0})$$

---

## Component Maps

**Scaling factors:**
$$f_m = \frac{\dot{m}_{C,\mathrm{dp}}}{\dot{m}_{C,\mathrm{udp}}}, \quad f_{\mathrm{PR}} = \frac{\pi_{C,\mathrm{dp}} - 1}{\pi_{C,\mathrm{udp}} - 1}, \quad f_{\eta} = \frac{\eta_{C,\mathrm{dp}}}{\eta_{C,\mathrm{udp}}}$$

**Scaled maps:**
$$\dot{m}_{C,\mathrm{scaled}} = f_m \cdot \dot{m}_{C,\mathrm{ref}}$$
$$\pi_{C,\mathrm{scaled}} = 1 + f_{\mathrm{PR}} (\pi_{C,\mathrm{ref}} - 1)$$
$$\eta_{C,\mathrm{scaled}} = f_{\eta} \cdot \eta_{C,\mathrm{ref}}$$

---

## Turbine Map Scaling

**Scaling factors:**
$$f_m = \frac{\dot{m}_{T,\mathrm{dp}}}{\dot{m}_{T,\mathrm{udp}}}, \quad f_{\mathrm{PR}} = \frac{\pi_{T,\mathrm{dp}} - 1}{\pi_{T,\mathrm{udp}} - 1}, \quad f_{\eta} = \frac{\eta_{T,\mathrm{dp}}}{\eta_{T,\mathrm{udp}}}$$

**Scaled maps:**
$$\dot{m}_{T,\mathrm{scaled}} = f_m \cdot \dot{m}_{T,\mathrm{ref}}$$
$$\pi_{T,\mathrm{scaled}} = 1 + f_{\mathrm{PR}} (\pi_{T,\mathrm{ref}} - 1)$$
$$\eta_{T,\mathrm{scaled}} = f_{\eta} \cdot \eta_{T,\mathrm{ref}}$$

---

## Off-Design Analysis

**Throttle:**
$$\tau_{\mathrm{th,OD}} = \tau_{\mathrm{th,DP}} \cdot \mathrm{th}$$

---

## Newton-Raphson

$$\mathbf{X}^{(k+1)} = \mathbf{X}^{(k)} - J^{-1}(\mathbf{X}^{(k)})\mathbf{F}(\mathbf{X}^{(k)})$$
