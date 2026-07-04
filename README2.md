# Single-Spool Turbojet Performance Framework

This document contains the mathematical and thermodynamic formulation for the Design Point (DP) and Off-Design (OD) analysis of a single-spool turbojet engine[cite: 8].

---

## 🛠️ Input Variables & Reference Parameters

### Geometry & Operating Conditions
* $A_1$: Compressor inlet area[cite: 8]
* $A_e$: Exhaust nozzle exit area ($A_5$)[cite: 8]
* $M_0, p_0, T_0$: Free-stream flight Mach number, static pressure, and static temperature[cite: 8]
* $\dot{m}_f$: Fuel mass flow rate[cite: 8]
* $Q_f$: Fuel lower heating value (LHV)[cite: 8]

### Fluid Properties & Efficiencies
* $\gamma, c_p$: Ratio of specific heats and specific heat at constant pressure for ambient/compressor air[cite: 8]
* $\gamma', c_p'$: Thermodynamic properties for high-temperature burned gases[cite: 8]
* $\eta_{\mathrm{IN}}, \eta_N$: Isentropic efficiencies of the intake and exhaust nozzle[cite: 8]
* $T_{\mathrm{ref}}, p_{\mathrm{ref}}$: Standard reference temperature and pressure used for component map scaling[cite: 8]

---

## 📈 1. Design Point (DP) Analysis

At the Design Point, initial stagnation conditions are determined, and the thermodynamic evolution through the components is calculated using nominal design parameters[cite: 8].

### Free-Stream Stagnation Conditions
The stagnation properties of the undisturbed air are computed from the flight Mach number $M_0$[cite: 8]:

$$T_{00} = T_0 \left(1 + \frac{(\gamma-1)}{2} M_0^2\right)$$

$$p_{00} = p_0 \left(1 + \frac{(\gamma-1)}{2} M_0^2\right)^{\frac{\gamma}{\gamma-1}}$$

### Intake (Station 0 → 1)
Assuming an intake with a specified isentropic efficiency $\eta_{\mathrm{IN}}$, the conditions at the compressor inlet are[cite: 8]:

$$T_{10} = T_{00}, \quad p_{10} = p_{00}$$

### Compressor (Station 1 → 2)
Given the target design pressure ratio $\pi_C = 10$ and isentropic efficiency $\eta_C = 0.85$[cite: 8]:

$$\tau_C = 1 + \frac{1}{\eta_C} \left( \pi_C^{\frac{(\gamma-1)}{\gamma}} - 1 \right)$$

$$T_{20} = \tau_C \cdot T_{10}$$

$$p_{20} = \pi_C \cdot p_{10}$$

### Combustion Chamber (CC / Station 2 → 3)
Combustion is modeled at constant pressure (burner pressure ratio $\pi_B = 1.0$)[cite: 8]. The turbine inlet temperature ($T_{30}$) is derived from the energy balance[cite: 8]:

$$p_{30} = p_{20}$$

$$T_{30} = \frac{f \cdot Q_f + c_p T_{20}}{(1+f) c_p'}$$

$$\tau_B = \frac{T_{30}}{T_{20}}, \quad \pi_B = \frac{p_{30}}{p_{20}} = 1.0$$

### Turbine (Station 3 → 4)
From the shaft power balance, the mechanical power extracted by the turbine must balance the power absorbed by the compressor ($P_T = P_C$)[cite: 8]:

$$(1+f) c_p' (T_{30} - T_{40}) = c_p (T_{20} - T_{10})$$

Solving for the temperature and pressure ratios across the turbine[cite: 8]:

$$\tau_T = 1 - \frac{c_p}{c_p' \cdot \tau_B \cdot (1+f)} \left(1 - \frac{1}{\tau_C}\right)$$

$$\pi_T = \left[ 1 - \frac{1}{\eta_T}(1 - \tau_T) \right]^{\frac{\gamma'}{\gamma'-1}}$$

$$T_{40} = \tau_T \cdot T_{30}, \quad p_{40} = \pi_T \cdot p_{30}$$

### Exhaust Nozzle (Station 4 → 5)
Without afterburning, the nozzle receives the gas at the turbine discharge conditions[cite: 8]:

$$T_{50} = T_{40}, \quad p_{50} = p_{40}$$

Defining the nozzle expansion ratio $\beta$ and the critical pressure ratio $\beta^*$[cite: 8]:

$$\beta = \frac{p_a}{p_{50}}$$

$$\beta^* = \frac{p^*}{p_{50}} = \left( \frac{\gamma'+1}{2} \right)^{-\frac{\gamma'}{\gamma'-1}}$$

* **Unchoked / Subcritical Nozzle** ($\beta > \beta^*$):[cite: 8]
  $$p_5 = p_a$$
  $$M_5 = \sqrt{\frac{2}{\gamma'-1} \left[ \left(\frac{1}{\beta}\right)^{\frac{\gamma'-1}{\gamma'}} - 1 \right]}$$

* **Choked / Critical Nozzle** ($\beta \le \beta^*$):[cite: 8]
  $$p_5 = p^* = p_{50} \cdot \beta^*$$
  $$M_5 = 1.0$$

---

## ⚙️ 2. Off-Design (OD) Analysis & Component Matching

During Off-Design maneuvers, the independent inputs are the compressor corrected mass flow $\dot{m}_C$, the turbine expansion ratio $\pi_T$, the corrected speed $N_C\%$, and the throttle setting.

### Mass Flow Rate & Compressor Performance
The actual physical air mass flow rate is calculated using local non-dimensional parameters[cite: 8]:

$$\dot{m}_a = \dot{m}_C \frac{\delta_1}{\sqrt{\theta_1}}$$

The actual values for $\pi_C$ and $\eta_C$ are extracted from the compressor performance maps based on the current operating point ($N_C\%$, $\dot{m}_C$)[cite: 8]:

$$\pi_C = \mathrm{map}_C(\dot{m}_C, N_C\%)$$

$$\eta_C = \mathrm{map}_C(\pi_C, N_C\%)$$

$$\tau_C = 1 + \frac{1}{\eta_C} \left( \pi_C^{\frac{(\gamma-1)}{\gamma}} - 1 \right)$$

$$T_{20} = \tau_C T_{10}, \quad p_{20} = \pi_C p_{10}$$

### Combustion Chamber & Throttle Inputs
The turbine inlet temperature varies according to the throttle input setting[cite: 8]:

$$T_{30} = \tau_{\mathrm{th}} T_{10}$$

$$f = \frac{c_p' T_{30} - c_p T_{20}}{Q_f - c_p' T_{30}}$$

$$\dot{m}_{\mathrm{gc}} = (1+f)\dot{m}_a, \quad p_{30} = \pi_B p_{20}$$

### Turbine Matching
The turbine rotational speed is scaled based on the new thermal balance relative to the design point[cite: 8]:

$$N_T\% = N_C\% \sqrt{\frac{\tau_{\mathrm{th,des}}}{\tau_{\mathrm{th}}}}$$

The corrected mass flow and isentropic efficiency are interpolated from the turbine performance maps[cite: 8]:

$$\dot{m}_T = \mathrm{map}_T(\pi_T, N_T\%)$$

$$\eta_T = \mathrm{map}_T(\pi_T, N_T\%)$$

$$\tau_T = 1 - \eta_T \left( 1 - \pi_T^{\frac{(\gamma'-1)}{\gamma'}} \right)$$

$$T_{40} = \tau_T T_{30}, \quad p_{40} = \pi_T p_{30}$$

### Nozzle Expansion (OD)

$$T_{50} = T_{40}, \quad p_{50} = p_{40} \pi_N$$

Applying the same sonic choking logic ($\beta$ vs $\beta^*$), the physical properties at the nozzle exit plane are computed[cite: 8]:

$$T_5 = \frac{T_{50}}{1 + \frac{(\gamma'-1)}{2} M_5^2}$$

$$a_5 = \sqrt{\gamma' R' T_5}, \quad V_5 = M_5 a_5$$

---

## ⚖️ 3. Congruence Equations (Non-Linear Programming Residuals)

The multi-dimensional iterative solver (e.g., Newton-Raphson) adjusts the state vector until the residuals of the physical conservation laws reach zero[cite: 8]:

1. **Turbine Mass Flow Continuity:**[cite: 8]
   $$\dot{m}_{T,\mathrm{map}} = \dot{m}_{\mathrm{gc}} \frac{\sqrt{\theta_3}}{\delta_3}$$

2. **Nozzle Geometric Area Consistency:**[cite: 8]
   $$A_5 = \frac{\dot{m}_{\mathrm{gc}}}{\rho_5 V_5} = A_{5,\mathrm{dp}}$$

3. **Rotor Shaft Power Equilibrium (Spool Balance):**[cite: 8]
   $$\dot{m}_a c_p (T_{20} - T_{10}) = \dot{m}_{\mathrm{gc}} c_p' (T_{30} - T_{40})$$

---

## 🚀 4. Performance Metrics

Once the non-linear system achieves numerical convergence, the net thrust ($S$) and the Thrust Specific Fuel Consumption (**TSFC**) are evaluated[cite: 8]:

### Net Thrust ($S$)

$$S = \dot{m}_a \left[ (1+f)V_5 - V_0 \right] + A_e(p_5 - p_0)$$

### Thrust Specific Fuel Consumption (TSFC)

$$\text{TSFC} = \frac{\dot{m}_f}{S}$$
