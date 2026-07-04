# Single-Spool Turbojet Performance Framework

This document contains the mathematical and thermodynamic formulation for the Design Point (DP) and Off-Design (OD) analysis of a single-spool turbojet engine.

---

# 🛠️ Input Variables & Reference Parameters

## Geometry & Operating Conditions

- $A_1$: Compressor inlet area
- $A_e$: Exhaust nozzle exit area ($A_5$)
- $M_0,\; p_0,\; T_0$: Free-stream flight Mach number, static pressure, and static temperature
- $\dot{m}_f$: Fuel mass flow rate
- $Q_f$: Fuel lower heating value (LHV)

## Fluid Properties & Efficiencies

- $\gamma,\; c_p$: Ratio of specific heats and specific heat at constant pressure for ambient/compressor air
- $\gamma',\; c_p'$: Thermodynamic properties for burned gases
- $\eta_{\mathrm{IN}},\; \eta_N$: Intake and nozzle isentropic efficiencies
- $T_{\mathrm{ref}},\; p_{\mathrm{ref}}$: Reference conditions for corrected maps

---

# 📈 1. Design Point (DP) Analysis

## Free-Stream Stagnation Conditions

$$
T_{00}=T_0\left(1+\frac{\gamma-1}{2}M_0^2\right)
$$

$$
p_{00}=p_0\left(1+\frac{\gamma-1}{2}M_0^2\right)^{\frac{\gamma}{\gamma-1}}
$$

---

## Intake (Station 0 → 1)

$$
T_{10}=T_{00},
\qquad
p_{10}=p_{00}
$$

---

## Compressor (Station 1 → 2)

Given

$$
\pi_C=10,
\qquad
\eta_C=0.85
$$

$$
\tau_C
=
1+
\frac{1}{\eta_C}
\left(
\pi_C^{\frac{\gamma-1}{\gamma}}
-1
\right)
$$

$$
T_{20}=\tau_C T_{10}
$$

$$
p_{20}=\pi_C p_{10}
$$

---

## Combustion Chamber

$$
p_{30}=p_{20}
$$

$$
T_{30}
=
\frac{
fQ_f+c_pT_{20}
}{
(1+f)c_p'
}
$$

$$
\tau_B=\frac{T_{30}}{T_{20}},
\qquad
\pi_B=\frac{p_{30}}{p_{20}}=1
$$

---

## Turbine

Power balance

$$
(1+f)c_p'
(T_{30}-T_{40})
=
c_p
(T_{20}-T_{10})
$$

Temperature ratio

$$
\tau_T
=
1-
\frac{
c_p
}{
c_p'
\tau_B
(1+f)
}
\left(
1-\frac1{\tau_C}
\right)
$$

Pressure ratio

$$
\pi_T
=
\left[
1-
\frac1{\eta_T}
(1-\tau_T)
\right]^{\frac{\gamma'}{\gamma'-1}}
$$

$$
T_{40}=\tau_TT_{30}
$$

$$
p_{40}=\pi_Tp_{30}
$$

---

## Exhaust Nozzle

$$
T_{50}=T_{40},
\qquad
p_{50}=p_{40}
$$

Expansion ratio

$$
\beta=\frac{p_a}{p_{50}}
$$

Critical pressure ratio

$$
\beta^*
=
\left(
\frac{\gamma'+1}{2}
\right)^{-\frac{\gamma'}{\gamma'-1}}
$$

### Unchoked nozzle

If

$$
\beta>\beta^*
$$

then

$$
p_5=p_a
$$

$$
M_5
=
\sqrt{
\frac{2}{\gamma'-1}
\left[
\left(\frac1\beta\right)^{\frac{\gamma'-1}{\gamma'}}
-1
\right]
}
$$

### Choked nozzle

If

$$
\beta\le\beta^*
$$

then

$$
p_5=p^*=p_{50}\beta^*
$$

$$
M_5=1
$$

---

# ⚙️ 2. Off-Design Analysis

## Compressor

$$
\dot{m}_a
=
\dot{m}_C
\frac{\delta_1}{\sqrt{\theta_1}}
$$

$$
\pi_C
=
\mathrm{map}_C(\dot{m}_C,N_C)
$$

$$
\eta_C
=
\mathrm{map}_C(\pi_C,N_C)
$$

$$
\tau_C
=
1+
\frac1{\eta_C}
\left(
\pi_C^{\frac{\gamma-1}{\gamma}}
-1
\right)
$$

$$
T_{20}=\tau_CT_{10}
$$

$$
p_{20}=\pi_Cp_{10}
$$

---

## Combustor

$$
T_{30}
=
\tau_{\mathrm{th}}T_{10}
$$

$$
f
=
\frac{
c_p'T_{30}
-
c_pT_{20}
}{
Q_f-c_p'T_{30}
}
$$

$$
\dot{m}_{gc}
=
(1+f)\dot{m}_a
$$

$$
p_{30}
=
\pi_Bp_{20}
$$

---

## Turbine

$$
N_T
=
N_C
\sqrt{
\frac{
\tau_{\mathrm{th,des}}
}{
\tau_{\mathrm{th}}
}
}
$$

$$
\dot{m}_T
=
\mathrm{map}_T(\pi_T,N_T)
$$

$$
\eta_T
=
\mathrm{map}_T(\pi_T,N_T)
$$

$$
\tau_T
=
1-
\eta_T
\left(
1-
\pi_T^{\frac{\gamma'-1}{\gamma'}}
\right)
$$

$$
T_{40}
=
\tau_TT_{30}
$$

$$
p_{40}
=
\pi_Tp_{30}
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
T_5
=
\frac{
T_{50}
}{
1+\frac{\gamma'-1}{2}M_5^2
}
$$

$$
a_5
=
\sqrt{\gamma'R'T_5}
$$

$$
V_5
=
M_5a_5
$$

---

# ⚖️ 3. Matching Equations

### Turbine mass-flow continuity

$$
\dot{m}_{T,\mathrm{map}}
=
\dot{m}_{gc}
\frac{\sqrt{\theta_3}}{\delta_3}
$$

### Nozzle area

$$
A_5
=
\frac{
\dot{m}_{gc}
}{
\rho_5V_5
}
=
A_{5,\mathrm{DP}}
$$

### Shaft power balance

$$
\dot{m}_a
c_p
(T_{20}-T_{10})
=
\dot{m}_{gc}
c_p'
(T_{30}-T_{40})
$$

---

# 🚀 4. Performance Metrics

## Net Thrust

$$
S
=
\dot{m}_a
\left[
(1+f)V_5
-
V_0
\right]
+
A_e(p_5-p_0)
$$

## Thrust Specific Fuel Consumption (TSFC)

$$
\mathrm{TSFC}
=
\frac{\dot{m}_f}{S}
$$
