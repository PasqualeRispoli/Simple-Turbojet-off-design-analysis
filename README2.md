# Single-Spool Turbojet Performance Framework

This document contains the mathematical and thermodynamic formulation for the Design Point (DP) and Off-Design (OD) analysis of a single-spool turbojet engine.

---

# 🛠️ Input Variables & Reference Parameters

## Geometry & Operating Conditions

- $A_1$: Compressor inlet area  
- $A_e$: Exhaust nozzle exit area ($A_5$)  
- $M_0, p_0, T_0$: Free-stream Mach number, static pressure, static temperature  
- $\dot{m}_f$: Fuel mass flow rate  
- $Q_f$: Fuel lower heating value  

## Fluid Properties & Efficiencies

- $\gamma, c_p$: Ambient/compressor gas properties  
- $\gamma', c_p'$: Combustion gas properties  
- $\eta_{\mathrm{IN}}, \eta_N$: Intake and nozzle efficiencies  
- $T_{\mathrm{ref}}, p_{\mathrm{ref}}$: Reference conditions  

---

# 📈 1. Design Point (DP) Analysis

## Free-stream stagnation

$$
T_{00}=T_0\left(1+\frac{\gamma-1}{2}M_0^2\right)
$$

$$
p_{00}=p_0\left(1+\frac{\gamma-1}{2}M_0^2\right)^{\frac{\gamma}{\gamma-1}}
$$

---

## Intake

$$
T_{10}=T_{00}, \quad p_{10}=p_{00}
$$

---

## Compressor

$$
\pi_C=10, \quad \eta_C=0.85
$$

$$
\tau_C = 1 + \frac{1}{\eta_C}\left(\pi_C^{\frac{\gamma-1}{\gamma}} - 1\right)
$$

$$
T_{20}=\tau_C T_{10}, \quad p_{20}=\pi_C p_{10}
$$

---

## Combustor

$$
p_{30}=p_{20}
$$

$$
T_{30}=\frac{fQ_f + c_p T_{20}}{(1+f)c_p'}
$$

$$
\tau_B=\frac{T_{30}}{T_{20}}, \quad \pi_B=1
$$

---

## Turbine

$$
(1+f)c_p'(T_{30}-T_{40}) = c_p(T_{20}-T_{10})
$$

$$
\tau_T = 1 - \frac{c_p}{c_p' \tau_B (1+f)}\left(1-\frac{1}{\tau_C}\right)
$$

$$
\pi_T = \left[1 - \frac{1}{\eta_T}(1-\tau_T)\right]^{\frac{\gamma'}{\gamma'-1}}
$$

$$
T_{40}=\tau_T T_{30}, \quad p_{40}=\pi_T p_{30}
$$

---

## Nozzle

$$
T_{50}=T_{40}, \quad p_{50}=p_{40}
$$

$$
\beta=\frac{p_a}{p_{50}}, \quad \beta^*=\left(\frac{\gamma'+1}{2}\right)^{-\frac{\gamma'}{\gamma'-1}}
$$

### Unchoked

$$
p_5=p_a
$$

$$
M_5=\sqrt{\frac{2}{\gamma'-1}\left[\left(\frac{1}{\beta}\right)^{\frac{\gamma'-1}{\gamma'}}-1\right]}
$$

### Choked

$$
p_5=p_{50}\beta^*, \quad M_5=1
$$

---

# ⚙️ 2. Off-Design Analysis

## Compressor

$$
\dot{m}_a=\dot{m}_C \frac{\delta_1}{\sqrt{\theta_1}}
$$

$$
\pi_C=\mathrm{map}_C(\dot{m}_C, N_C)
$$

$$
\eta_C=\mathrm{map}_C(\pi_C, N_C)
$$

$$
\tau_C=1+\frac{1}{\eta_C}\left(\pi_C^{\frac{\gamma-1}{\gamma}}-1\right)
$$

$$
T_{20}=\tau_C T_{10}, \quad p_{20}=\pi_C p_{10}
$$

---

## Combustor

$$
T_{30}=\tau_{\mathrm{th}} T_{10}
$$

$$
f=\frac{c_p' T_{30}-c_p T_{20}}{Q_f - c_p' T_{30}}
$$

$$
\dot{m}_{gc}=(1+f)\dot{m}_a
$$

$$
p_{30}=\pi_B p_{20}
$$

---

## Turbine

$$
N_T = N_C \sqrt{\frac{\tau_{\mathrm{th,des}}}{\tau_{\mathrm{th}}}}
$$

$$
\dot{m}_T=\mathrm{map}_T(\pi_T, N_T)
$$

$$
\eta_T=\mathrm{map}_T(\pi_T, N_T)
$$

$$
\tau_T=1-\eta_T\left(1-\pi_T^{\frac{\gamma'-1}{\gamma'}}\right)
$$

$$
T_{40}=\tau_T T_{30}, \quad p_{40}=\pi_T p_{30}
$$

---

## Nozzle

$$
T_{50}=T_{40}
$$

$$
p_{50}=p_{40}\pi_N
$$

$$
T_5=\frac{T_{50}}{1+\frac{\gamma'-1}{2}M_5^2}
$$

$$
a_5=\sqrt{\gamma' R' T_5}
$$

$$
V_5=M_5 a_5
$$

---

# ⚖️ 3. Matching Equations

## Turbine mass flow

$$
\dot{m}_{T,\mathrm{map}}=\dot{m}_{gc}\frac{\sqrt{\theta_3}}{\delta_3}
$$

## Nozzle area

$$
A_5=\frac{\dot{m}_{gc}}{\rho_5 V_5}=A_{5,\mathrm{DP}}
$$

## Shaft balance

$$
\dot{m}_a c_p (T_{20}-T_{10})=\dot{m}_{gc} c_p'(T_{30}-T_{40})
$$

---

# 🚀 4. Performance Metrics

## Net thrust

$$
S=\dot{m}_a\left[(1+f)V_5 - V_0\right]+A_e(p_5-p_0)
$$

## TSFC

$$
\mathrm{TSFC}=\frac{\dot{m}_f}{S}
$$
