import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import PchipInterpolator



class Turbine():

    def __init__(self):


        self.N_corr_ref = np.array([5000, 6000, 7000, 8000, 9000, 10000, 11000])


        # Pr as a function of m_dot_corr_ref and N_corr_ref 
        self.m_dot_corr_ref = np.array([[40.403, 44.417, 46.653, 47.966, 48.97, 49.544, 50.001, 50.081, 50.086, 50.095, 50.09, 50.0922],
                                [40.044, 43.754, 46.125, 47.626, 48.513, 49.105, 49.481, 49.58, 49.597, 49.624, 49.638, 49.633],
                                [39.941, 43.795, 46.017, 47.335, 48.795, 49.199, 49.279, 49.27, 49.248, 49.23, 49.255, 49.2428],
                                [39.896, 43.512, 45.914, 47.061, 48.011, 48.558, 48.943, 49.042, 49.069, 49.01, 49.046, 49.0266],
                                [39.524, 42.934, 45.686, 46.743, 47.715, 48.67, 48.777, 48.836, 48.876, 48.836, 48.845, 48.8184],
                                [39.439, 43.01, 45.556, 46.801, 47.792, 48.388, 48.634, 48.67, 48.639, 48.647, 48.625, 48.5912],
                                [39.502, 42.849, 45.336, 46.385, 47.312, 47.877, 48.222, 48.397, 48.459, 48.482, 48.455, 48.414]])

        self.PR_beta = np.array([[1.217, 1.285, 1.323, 1.363, 1.402, 1.427, 1.495, 1.545, 1.6, 1.687, 1.747, 1.8074],
                            [1.231, 1.302, 1.356, 1.404, 1.443, 1.473, 1.525, 1.577, 1.635, 1.709, 1.782, 1.845],
                            [1.242, 1.328, 1.388, 1.437, 1.528, 1.617, 1.704, 1.811, 1.915, 1.979, 2.053, 2.1226],
                            [1.244, 1.339, 1.417, 1.465, 1.528, 1.584, 1.692, 1.787, 1.899, 2, 2.075, 2.1492],
                            [1.245, 1.34, 1.425, 1.492, 1.546, 1.684, 1.748, 1.882, 1.987, 2.084, 2.167, 2.2458],
                            [1.251, 1.345, 1.442, 1.521, 1.596, 1.692, 1.849, 1.972, 2.1, 2.173, 2.259, 2.3424],
                            [1.248, 1.348, 1.447, 1.516, 1.581, 1.651, 1.749, 1.839, 1.93, 2.024, 2.154, 2.242]])

        #------------------------------------------------------------------------------------------------------------------------------

        # PR mi serve per la mappa delle efficienze
        self.PR_eta = np.array( [[1.224, 1.246, 1.292, 1.387, 1.457, 1.534, 1.61, 1.686, 1.743, 1.79, 1.871, 1.914],
                        [1.237, 1.25, 1.28, 1.369, 1.459, 1.553, 1.629, 1.716, 1.799, 1.846, 1.927, 1.97],
                        [1.241, 1.255, 1.283, 1.326, 1.401, 1.509, 1.591, 1.704, 1.806, 1.913, 1.994, 2.037],
                        [1.25, 1.265, 1.308, 1.364, 1.456, 1.532, 1.637, 1.739, 1.851, 1.934, 2.042, 2.085],
                        [1.281, 1.314, 1.371, 1.425, 1.498, 1.574, 1.647, 1.749, 1.878, 1.979, 2.091, 2.18],
                        [1.252, 1.328, 1.425, 1.544, 1.642, 1.757, 1.873, 2.005, 2.1, 2.204, 2.248, 2.28],
                        [1.382, 1.43, 1.495, 1.586, 1.688, 1.791, 1.887, 1.99, 2.079, 2.158, 2.249, 2.217]])


        self.eta = np.array([[.72, .754, .759, .739, .714, .679, .643, .603, .554, .524, .494, .48],
                        [.716, .757, .794, .819, .812, .788, .761, .728, .692, .662, .632, .618],
                        [.629, .691, .775, .831, .858, .869, .859, .842, .816, .782, .752, .738],
                        [.594, .668, .757, .804, .857, .883, .892, .893, .884, .865, .835, .821],
                        [.664, .72, .779, .823, .858, .883, .897, .905, .904, .896, .883, .868],
                        [.559, .61, .673, .741, .788, .835, .869, .895, .908, .899, .854, .751],
                        [.718, .785, .824, .855, .882, .9, .908, .906, .884, .857, .804, .701]])     
            

        #------------------------------------------------------------------------------------------------------------------------------

    def unscaled_dp(self):
        N_udp = 8000
        PR_udp = 1.8
        
        m_udp = self.map_interpolator("PR", scaled=False ,N=N_udp, x=PR_udp)
        eta_udp = self.map_interpolator("eta", scaled=False ,N=N_udp, x=PR_udp)
        N_perc_list = self.N_corr_ref/N_udp
        
        return N_perc_list, PR_udp, m_udp ,eta_udp
    
    def scale_map(self, m_dp, PR_dp, eta_dp):
        N_perc_list, PR_udp, m_udp ,eta_udp = self.unscaled_dp()
        
        f_m = m_dp/m_udp
        f_PR = (PR_dp-1)/(PR_udp-1)
        f_eta = eta_dp/eta_udp

        self.N_perc_list = N_perc_list
        
        self.PR_beta_scaled = 1 + f_PR*(self.PR_beta-1)
        self.m_scaled = f_m*self.m_dot_corr_ref
       
        self.PR_eta_scaled = 1 + f_PR*(self.PR_eta-1)
        self.eta_scaled = f_eta*self.eta 


    def map_interpolator(self, map_type: dict ,scaled: bool ,N, x):

        if not scaled:
            N_list = self.N_corr_ref
            if map_type == "PR":
                x_list = self.PR_beta
                y_list = self.m_dot_corr_ref
            elif map_type == "eta":
                x_list = self.PR_eta
                y_list = self.eta
        elif scaled:
            N_list = self.N_perc_list
            if map_type == "PR":
                x_list = self.PR_beta_scaled
                y_list = self.m_scaled
            elif map_type == "eta":
                x_list = self.PR_eta_scaled
                y_list = self.eta_scaled


        if N < np.min(N_list) or N > np.max(N_list):
                raise Exception("NUMERO DI GIRI TURBINA FUORI DAL RANGE DELLA MAPPA")

        # given N voglio sapere in che range è compreso:
    
        for i in np.arange(len(N_list)-1):
            if N >= N_list[i] and N <= N_list[i+1]:
                #calcolare la % di distanza tra le due isocurve N
                perc = (N-N_list[i])/(N_list[i+1]-N_list[i])
                x_perc = x_list[i] + perc*(x_list[i+1] - x_list[i]) #è un vettore contenente le mdot dei punti a distanza %p
                y_perc = y_list[i] + perc*(y_list[i+1] - y_list[i]) #è un vettore contenente le beta dei punti a distanza %p
                #faccio la spline passante per questi punti
                break
                
        Df = pd.DataFrame({ "y_perc": y_perc,"x_perc": x_perc})
                
        Df.sort_values(by=["x_perc"], inplace=True)
        x_perc = Df["x_perc"].values
        y_perc = Df["y_perc"].values

        spline_perc = PchipInterpolator(x_perc, y_perc, extrapolate=True)
                
        
        y =  spline_perc(x)       

        return y
    
        
   
    
    def dispmap(self, map_type ,scaled: bool ,x = np.nan , y = np.nan, linetype="-*"):                   
        
        if not scaled:
            N_list = self.N_corr_ref
            if map_type == "PR":
                x_list = self.PR_beta
                y_list = self.m_dot_corr_ref
            elif map_type == "eta":
                x_list = self.PR_eta
                y_list = self.eta
        elif scaled:
            N_list = self.N_perc_list
            if map_type == "PR":
                x_list = self.PR_beta_scaled
                y_list = self.m_scaled
            elif map_type == "eta":
                x_list = self.PR_eta_scaled
                y_list = self.eta_scaled
        

        for i,k in enumerate(x_list):
            plt.plot(k, y_list[i])
            
        plt.plot(x,y,linetype)