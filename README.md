# Simple Turbojet Off-Design Analysis

A Python-based simulation tool for analyzing single-spool turbojet performance at both design point and off-design operating conditions. This code implements thermodynamic analysis of turbojet components and map-based off-design solution methods.

---

# Overview

This project performs detailed thermodynamic analysis of a turbojet engine consisting of:

- **Inlet**: compresses incoming air at flight conditions  
- **Compressor**: increases pressure and temperature  
- **Combustor (CC)**: burns fuel and adds thermal energy  
- **Turbine**: extracts work to drive compressor  
- **Nozzle**: converts enthalpy into thrust  

Two operating regimes:

1. **Design Point (DP)**: reference condition  
2. **Off-Design (OD)**: solved via Newton-Raphson coupling

---

# Design Point Analysis

## Input Parameters

```python
M_0 = 0.7
p_0 = 41059
T_0 = 242
mdot_a = 20.0
pi_C = 8.3
eta_C = 0.822
eta_T = 0.88
f = 0.02
Q_f = 43.26e6
```

---

## Thermodynamic Properties

| Property | Value |
|----------|------|
| γ (air) | 1.4 |
| γ_gc | 1.33 |
| R | 287 |
| R_gc | 293 |
| c_p | 1004 |
| c_p,gc | 1184 |

---

# Stage 0: Inlet

$$
a_0 = \sqrt{\gamma R T_0}
$$

$$
V_0 = M_0 a_0
$$

$$
p_{0,0} = p_0 \left(1 + \frac{\gamma-1}{2}M_0^2\right)^{\frac{\gamma}{\gamma-1}}
$$

$$
T_{0,0} = T_0 \left(1 + \frac{\gamma-1}{2}M_0^2\right)
$$

$$
\rho_0 = \frac{p_0}{R T_0}
$$

$$
A_0 = \frac{\dot{m}_a}{\rho_0 V_0}
$$

---

# Stage 1-2: Compressor

$$
\tau_C = 1 + \frac{1}{\eta_C}\left(\pi_C^{\frac{\gamma-1}{\gamma}} - 1\right)
$$

$$
T_{2,0} = \tau_C T_{1,0}
$$

$$
p_{2,0} = \pi_C p_{1,0}
$$

$$
\dot{m}_{C,corr} = \dot{m}_a \frac{\sqrt{\theta_1}}{\delta_1}
$$

$$
\theta_1 = \frac{T_{1,0}}{T_{ref}}, \quad \delta_1 = \frac{p_{1,0}}{p_{ref}}
$$

---

# Stage 2-3: Combustor

$$
p_{3,0} = p_{2,0}
$$

$$
T_{3,0} = \frac{f Q_f + c_p T_{2,0}}{(1+f)c_{p,gc}}
$$

$$
\tau_B = \frac{T_{3,0}}{T_{2,0}}, \quad \pi_B = 1
$$

$$
\dot{m}_{gc} = (1+f)\dot{m}_a
$$

$$
\dot{m}_{T,corr} = \dot{m}_{gc} \frac{\sqrt{\theta_3}}{\delta_3}
$$

---

# Stage 3-4: Turbine

$$
\tau_T = 1 - \frac{c_p}{c_{p,gc}(1+f)\tau_B}\left(1 - \frac{1}{\tau_C}\right)
$$

$$
\pi_T = \left[1 - \frac{1}{\eta_T}(1 - \tau_T)\right]^{\frac{\gamma_{gc}}{\gamma_{gc}-1}}
$$

$$
T_{4,0} = \tau_T T_{3,0}
$$

$$
p_{4,0} = \pi_T p_{3,0}
$$

---

# Stage 4-5: Nozzle

$$
\beta_{cr} = \left(\frac{\gamma_{gc}+1}{2}\right)^{-\frac{\gamma_{gc}}{\gamma_{gc}-1}}
$$

$$
\beta = \frac{p_0}{p_{5,0}}
$$

### Subsonic

$$
p_5 = p_0
$$

$$
M_5 = \sqrt{\frac{2}{\gamma_{gc}-1}\left[\left(\frac{1}{\beta}\right)^{\frac{\gamma_{gc}-1}{\gamma_{gc}}} - 1\right]}
$$

### Choked

$$
M_5 = 1
$$

$$
p_5 = \frac{p_{5,0}}{\beta_{cr}}
$$

---

# Exit Flow

$$
T_5 = \frac{T_{5,0}}{1 + \frac{\gamma_{gc}-1}{2}M_5^2}
$$

$$
a_5 = \sqrt{\gamma_{gc} R_{gc} T_5}
$$

$$
V_5 = M_5 a_5
$$

$$
\rho_5 = \frac{p_5}{R_{gc} T_5}
$$

$$
A_5 = \frac{\dot{m}_{gc}}{\rho_5 V_5}
$$

---

# Performance

## Thrust

$$
S = \dot{m}_a(1+f)V_5 - \dot{m}_a V_0 + A_5(p_5 - p_0)
$$

## Compressor power

$$
P_{ex} = \dot{m}_a c_p(T_{2,0}-T_{1,0}) - \dot{m}_a(1+f)c_{p,gc}(T_{3,0}-T_{4,0})
$$

---

# Component Maps

## Scaling factors

$$
f_m = \frac{\dot{m}_{C,dp}}{\dot{m}_{C,ref}}, \quad
f_{PR} = \frac{\pi_{C,dp}-1}{\pi_{C,ref}-1}, \quad
f_\eta = \frac{\eta_{C,dp}}{\eta_{C,ref}}
$$

## Scaled maps

$$
\dot{m}_C = f_m \dot{m}_{ref}
$$

$$
\pi_C = 1 + f_{PR}(\pi_{ref}-1)
$$

$$
\eta_C = f_\eta \eta_{ref}
$$

---

# Off-Design Analysis

## Throttle

$$
\tau_{th,OD} = \tau_{th,DP} \cdot th
$$

---

## Residual equations

### 1. Turbine matching

$$
f_1 = \frac{\dot{m}_{T,corr} - (1+f)\dot{m}_a \frac{\sqrt{\theta_3}}{\delta_3}}{\dot{m}_{T,dp,corr}}
$$

### 2. Nozzle area

$$
f_2 = \frac{A_{5,dp} - A_5}{A_{5,dp}}
$$

### 3. Power balance

$$
f_3 = \frac{\dot{m}_a c_p (T_{2,0}-T_{1,0})}{\dot{m}_a(1+f)c_{p,gc}(T_{3,0}-T_{4,0})} - 1
$$

---

# Newton-Raphson

$$
X^{k+1} = X^k - J^{-1}(X^k)F(X^k)
$$

$$
J_{ij} \approx \frac{f_i(x_j+\epsilon)-f_i(x_j)}{\epsilon}
$$

---

# Code Structure

## MAIN_SP.py
- DesignPoint()
- Off_Design()
- Jacobian()
- F(X)

## Compressor_map.py / Turbine_map.py
- scale_map()
- map_interpolator()
- dispmap()

---

# Key Insights

- Single spool ⇒ strong coupling compressor/turbine  
- throttle controls thermal ratio  
- map interpolation introduces nonlinear behavior  
- nozzle choking is limiting constraint  
- NR solves full coupled system  

---
