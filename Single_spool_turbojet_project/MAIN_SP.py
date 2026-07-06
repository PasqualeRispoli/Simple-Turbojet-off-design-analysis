import numpy as np
from Compressor_map import Compressor
from Turbine_map import Turbine
from matplotlib import pyplot as plt
import pandas as pd 
from scipy import linalg


C = Compressor()
T = Turbine()
T_ref = 273 
p_ref = 101315
cp = 1004 
cp_gc = 1184
gamma = 1.4
gamma_gc = 1.33
R = 287
R_gc = 293
Q_f = 43260000 


print(
    """
====================================================================
 Execution of Design Point of: SINGLE SPOOL TURBOJET
====================================================================        
    """
)

##
###


def DesignPoint():

    global T_ref
    global p_ref 
    
    global cp 
    global cp_gc
    global gamma
    global gamma_gc
    global R
    global R_gc
    global Q_f
    
    
    M_0 = 0.7 
    p_0 = 41059 #Pa
    T_0 = 242
    m_a = 20 #kg/s
    pi_C= 8.3
    eta_C = 0.822
    eta_T =0.88
    f = 0.02
    

    
    a_0 = np.sqrt(gamma*R*T_0)
    V_0 = M_0*a_0 
    
    p_0_0 = p_0*(1+ (gamma-1)/2*M_0**2)**(gamma/(gamma-1))
    T_0_0 = T_0*(1+ (gamma-1)/2*M_0**2)
    rho_0 = p_0/(R*T_0)
    
    A_0 = m_a/(rho_0*V_0)
    
    
    
    p_1_0 = p_0_0
    T_1_0 = T_0_0
    
    # Compressor
    tau_C = 1 + 1/eta_C*((pi_C**((gamma-1)/gamma))-1)
    
    T_2_0 = tau_C*T_1_0
    p_2_0 = pi_C*p_1_0 
    
    #CC
    p_3_0 = p_2_0
    T_3_0 = (f*Q_f+cp*T_2_0)/((1+f)*cp_gc)
    tau_B = T_3_0/T_2_0
    pi_B = p_3_0/p_2_0
    
    #Turbine
    tau_T = 1 - (cp/(cp_gc*tau_B*(1+f))) * (1- 1/tau_C)
    pi_T = (1 - 1/eta_T * (1-tau_T))**(gamma_gc/(gamma_gc-1))
    T_4_0 = tau_T*T_3_0
    p_4_0 = pi_T*p_3_0
    
    #Nozzle
    p_5_0 = p_4_0
    T_5_0 = T_4_0
    
    beta = p_0/p_5_0
    beta_cr = ((gamma_gc+1)/2)**((-gamma_gc)/(gamma_gc-1))
    
    if beta > beta_cr:
        p_5 = p_0
        M_5 = np.sqrt(((1/beta)**((gamma_gc-1)/gamma_gc) -1 )* 2/(gamma_gc-1))
    elif beta <= beta_cr:
        p_5 = p_5_0/beta_cr
        M_5 = 1
    
    T_5 = T_5_0/(1 + (gamma_gc-1)/2 * M_5**2)
    a_5 = np.sqrt(gamma_gc*R_gc*T_5)
    
    V_5 = M_5*a_5
    rho_5 = p_5/(R_gc*T_5)
    
    m_gc = (1+f)*m_a
    A_5 = m_gc/(rho_5*V_5)
    
        
    S = m_a*((1+f)*V_5 - V_0) + A_5*(p_5 - p_0)
    
    Pwr_ex = (m_a*cp*(T_2_0-T_1_0)) - m_a*(1+f)*cp_gc*(T_3_0-T_4_0)
    
    #------------------------------------------------------------------
    theta_1 = T_1_0/T_ref
    delta_1 = p_1_0/p_ref
    theta_3 = T_3_0/T_ref
    delta_3 = p_3_0/p_ref
    
    tau_th = T_3_0/T_1_0
    m_C = (m_a*np.sqrt(theta_1))/delta_1
    m_T = (m_gc*np.sqrt(theta_3))/delta_3
        
    DP_param = {}
    
    DP_param["M_0"] = M_0
    DP_param["p_0"] = p_0 
    DP_param["T_0"] = T_0
    DP_param["A_0"] = A_0
    DP_param["p_0_0"] = p_0_0
    DP_param["T_0_0"] = T_0_0
    DP_param["p_1_0"] = p_1_0
    DP_param["T_1_0"] = T_1_0
    DP_param["T_2_0"] = T_2_0
    DP_param["tau_C"] = tau_C
    DP_param["pi_C"] = pi_C
    DP_param["eta_C"] = eta_C
    DP_param["T_3_0"] = T_3_0
    DP_param["p_3_0"] = p_3_0
    DP_param["tau_B"] = tau_B
    DP_param["T_4_0"] = T_4_0
    DP_param["p_4_0"] = p_4_0
    DP_param["tau_T"] = tau_T
    DP_param["pi_T"] = pi_T
    DP_param["eta_T"] = eta_T
    DP_param["T_5_0"] = T_5_0
    DP_param["p_5_0"] = p_5_0
    DP_param["p_5"] = p_5
    DP_param["T_5"] = T_5
    DP_param["M_5"] = M_5
    DP_param["V_0"] = V_0
    DP_param["V_5"] = V_5
    DP_param["f"] = f
    DP_param["m_a"] = m_a
    DP_param["S"] = S
    DP_param["A_5"] = A_5
    DP_param["rho_0"] = rho_0
    DP_param["rho_5"] = rho_5
    DP_param["Pwr_ex"] = Pwr_ex
    DP_param["tau_th"] = tau_th
    DP_param["m_C"] = m_C
    DP_param["m_T"] = m_T
    

        
    return DP_param
                
    
DP = DesignPoint()

m_C_dp = DP["m_C"]
m_T_dp = DP["m_T"]
eta_C_dp = DP["eta_C"]
eta_T_dp = DP["eta_T"]
pi_C_dp = DP["pi_C"]
pi_T_dp = DP["pi_T"]
tau_th_dp = DP["tau_th"]

C.scale_map(m_dp=m_C_dp, PR_dp=pi_C_dp, eta_dp=eta_C_dp)
T.scale_map(m_dp=m_T_dp, PR_dp=1/pi_T_dp, eta_dp=eta_T_dp)




    
for i in DP:
    print(i,"=" ,DP[i])
    print("-------------")

print(
    """
====================================================================
 Execution of Off-Design Point of: SINGLE SPOOL TURBOJET
====================================================================        
    """
)


OD = dict()
th = 0.85 # perc of throttle to dp (1 for DP)
OD["tau_th"] = tau_th_dp*th

def Off_Design(DP, OD, m_C, N_C ,pi_T):
    
    tau_th = OD["tau_th"]
    
    global T_ref
    global p_ref
    global C
    global T
    
    global cp 
    global cp_gc
    global gamma
    global gamma_gc
    global R
    global R_gc
    global Q_f
   
    p_0 = DP["p_0"]
    T_0 = DP["T_0"]
    M_0 = DP["M_0"]
    V_0 = DP["V_0"]
    p_0_0 = DP["p_0_0"]
    T_0_0 = DP["T_0_0"]
    rho_0 = DP["rho_0"]
    T_1_0 = DP["T_1_0"]
    p_1_0 = DP["p_1_0"]
    theta_1 = T_1_0/T_ref
    delta_1 = p_1_0/p_ref
    
    m_a = (m_C*delta_1)/np.sqrt(theta_1)
    
    pi_C = C.map_interpolator(map_type="PR",scaled=True, N=N_C, x=m_C)
    eta_C = C.map_interpolator(map_type="eta",scaled=True, N=N_C, x=m_C)
    
    tau_C = 1 + (1/eta_C)*(pi_C**((gamma-1)/gamma) -1)
    T_2_0 = tau_C*T_1_0
    p_2_0 = pi_C*p_1_0
    

    
    T_3_0 = tau_th*T_1_0
    p_3_0 = p_2_0 
    f = (cp_gc*T_3_0 - cp*T_2_0)/(Q_f - cp_gc*T_3_0)
    m_gc = (1+f)*m_a
    

    theta_3 = T_3_0/T_ref
    delta_3 = p_3_0/p_ref
    
    
    tau_th_dp = DP["tau_th"]
    
    N_T = N_C*np.sqrt(tau_th_dp/tau_th)
    m_T = T.map_interpolator(map_type="PR", scaled=True, N=N_T, x=1/pi_T)
    eta_T = T.map_interpolator(map_type="eta", scaled=True, N=N_T, x=1/pi_T)
    tau_T = 1 - eta_T*(1 - pi_T**((gamma_gc-1)/gamma_gc))   
    
    
    T_4_0 = tau_T*T_3_0
    p_4_0 = pi_T*p_3_0  
    p_5_0 = p_4_0
    T_5_0 = T_4_0
    
    beta = p_0/p_5_0
    beta_cr = ((gamma_gc+1)/2)**((-gamma_gc)/(gamma_gc-1))
    
    
    if beta > beta_cr:
        p_5 = p_0
        M_5 = np.sqrt(((1/beta)**((gamma_gc-1)/gamma_gc) -1 )* 2/(gamma_gc-1))

    elif beta <= beta_cr:
        p_5 = p_5_0/beta_cr
        M_5 = 1

  
    
    T_5 = T_5_0/(1 + (gamma_gc-1)/2 * M_5**2)
    a_5 = np.sqrt(gamma_gc*R_gc*T_5)
    
    V_5 = M_5*a_5
    rho_5 = p_5/(R_gc*T_5)
    
    A_5 = m_gc/(rho_5*V_5)
    A_5_dp = DP["A_5"]
    
        
    f_1 = (m_T - (m_gc*np.sqrt(theta_3))/delta_3)/m_T_dp
    f_2 = (A_5_dp - A_5)/A_5_dp
    f_3 = (m_a*cp*(T_2_0-T_1_0))/(m_gc*cp_gc*(T_3_0 - T_4_0)) - 1
    
    #Params to add on OD dictionary
    A_0 = m_a/(rho_0*V_0)
    tau_B = T_3_0/T_2_0
    S = m_a*((1+f)*V_5 - V_0) + A_5*(p_5 - p_0)
    Pwr_ex = (m_a*cp*(T_2_0-T_1_0)) - m_a*(1+f)*cp_gc*(T_3_0-T_4_0)
    
    # writing OD points
    OD["M_0"] = M_0
    OD["p_0"] = p_0 
    OD["T_0"] = T_0
    OD["A_0"] = A_0
    OD["p_0_0"] = p_0_0
    OD["T_0_0"] = T_0_0
    OD["p_1_0"] = p_1_0
    OD["T_1_0"] = T_1_0
    OD["T_2_0"] = T_2_0
    OD["tau_C"] = tau_C
    OD["pi_C"] = pi_C
    OD["eta_C"] = eta_C
    OD["T_3_0"] = T_3_0
    OD["p_3_0"] = p_3_0
    OD["tau_B"] = tau_B
    OD["T_4_0"] = T_4_0
    OD["p_4_0"] = p_4_0
    OD["tau_T"] = tau_T
    OD["pi_T"] = pi_T
    OD["eta_T"] = eta_T
    OD["T_5_0"] = T_5_0
    OD["p_5_0"] = p_5_0
    OD["p_5"] = p_5
    OD["T_5"] = T_5
    OD["M_5"] = M_5
    OD["V_0"] = V_0
    OD["V_5"] = V_5
    OD["f"] = f
    OD["m_a"] = m_a
    OD["S"] = S
    OD["A_5"] = A_5
    OD["rho_0"] = rho_0
    OD["rho_5"] = rho_5
    OD["Pwr_ex"] = Pwr_ex
    OD["tau_th"] = tau_th
    OD["m_C"] = m_C
    OD["m_T"] = m_T
    OD["N_C"] = N_C
    OD["N_T"] = N_T
    
    
    
    return f_1, f_2, f_3


# X = [m_C, N_C, pi_T]

#f_1, f_2, f_3 = Off_Design(DP=DP, OD=OD, m_C=m_C_dp, N_C=1, pi_T=pi_T_dp)
# print(f_1, f_2, f_3)

def Jacobian(X_0: np.ndarray):
    global DP, OD
    eps = 1e-13
    
    f1_0, f2_0, f3_0 = Off_Design(DP=DP, OD=OD, m_C=X_0[0], N_C=X_0[1], pi_T= X_0[2])
    
    f1, f2, f3 = Off_Design(DP=DP, OD=OD, m_C=X_0[0]*(1+eps), N_C=X_0[1], pi_T= X_0[2]) 
    D_f1, D_f2, D_f3 = f1-f1_0, f2-f2_0, f3-f3_0 
    D_X0_1 = eps*X_0[0]
    f1_mc, f2_mc, f3_mc = D_f1/(D_X0_1), D_f2/(D_X0_1), D_f3/(D_X0_1) 
    
    
    f1, f2, f3 = Off_Design(DP=DP, OD=OD, m_C=X_0[0], N_C=X_0[1]*(1+eps), pi_T= X_0[2]) 
    D_f1, D_f2, D_f3 = f1-f1_0, f2-f2_0, f3-f3_0 
    D_X0_2 = eps*X_0[1]
    f1_NC, f2_NC, f3_NC = D_f1/(D_X0_2), D_f2/(D_X0_2), D_f3/(D_X0_2)
    
    
    f1, f2, f3 = Off_Design(DP=DP, OD=OD, m_C=X_0[0], N_C=X_0[1], pi_T= X_0[2]*(1+eps)) 
    D_f1, D_f2, D_f3 = f1-f1_0, f2-f2_0, f3-f3_0
    D_X0_3 = eps*X_0[2]
    f1_piT, f2_piT, f3_piT = D_f1/(D_X0_3), D_f2/(D_X0_3), D_f3/(D_X0_3)

    
    A = np.array([[f1_mc, f1_NC, f1_piT],
                  [f2_mc, f2_NC, f2_piT],
                  [f3_mc, f3_NC, f3_piT]])     
    
    
    return A

def F(X: np.ndarray):
    f_1, f_2, f_3 = Off_Design(DP=DP, OD=OD, m_C=X[0], N_C=X[1], pi_T=X[2])
    return np.array([f_1, f_2, f_3])

    

tol = 1e-14 

X_0 = np.array([m_C_dp, 1, pi_T_dp])
RES = 10
max_iter = 100
iter = 0

while RES > tol and iter < max_iter:

    A = Jacobian(X_0)
    B = A.dot(X_0) - F(X_0)
    X = np.linalg.solve(A,B)
    
    R_0 = np.array([X_0[0]/pi_C_dp, X_0[1], X_0[2]/pi_T_dp])
    R = np.array([X[0]/pi_C_dp, X[1], X[2]/pi_T_dp])
    
    norm_R0 = np.sum(R_0**2)
    norm_R = np.sum(R**2)
    
    RES = abs(norm_R-norm_R0)/norm_R0
    
    X_0 = X 
    iter = iter+1
    

print(f"-method converged in iter: {iter}")
print(f"-method residual: {RES}")
print(f"-result X_0:{X_0}")
    
m_C_od = X_0[0]
N_C_od = X_0[1]
pi_T_od = X_0[2]

       
#_,_,_, = Off_Design(DP, OD, m_C=m_C_od, N_C=N_C_od ,pi_T=pi_T_od)

for i in OD:
    print(i,"=" ,OD[i])
    print("-------------")

pi_C_od = OD["pi_C"]

    
    
C.dispmap(map_type="PR", scaled=True, x=[m_C_dp, m_C_od], y=[pi_C_dp, pi_C_od])
plt.show()
    