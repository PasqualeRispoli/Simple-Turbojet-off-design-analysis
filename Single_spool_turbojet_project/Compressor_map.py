import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import PchipInterpolator

class Compressor():


    def __init__(self):

        self.N_corr_ref = np.array([5000, 6000, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 11100])


        # Pr as a function of m_dot_corr_ref and N_corr_ref 

        self.PR_comp = np.array([[1.369, 1.459, 1.587, 1.654, 1.734, 1.775, 1.82], 
                    [1.918, 2.075, 2.229, 2.318, 2.405, 2.456, 2.481], 
                    [2.706, 2.966, 3.168, 3.334, 3.404, 3.445, 3.435], 
                    [3.203, 3.533, 3.833, 4.021, 4.127, 4.135, 4.066],
                    [3.782, 4.222, 4.565, 4.867, 5.065, 5.07, 4.934],
                    [4.302, 4.861, 5.285, 5.821, 6.161, 6.334, 6.142], 
                    [4.841, 5.445, 5.988, 6.628, 7.222, 7.623, 7.573], 
                    [5.358, 5.997, 6.589, 7.334, 8.012, 8.668, 9], 
                    [5.851, 6.491, 7.124, 7.982, 8.754, 9.57, 9.814],
                    [6.707, 7.321, 8.034, 9.047, 9.94, 10.834, 10.998]])


        self.eta = np.array([[.68, .69, .695, .7, .701, .705, .704],
                        [.7, .725, .75, .755, .745, .73, .725],
                        [.77, .795, .81, .805, .78, .765, .745],
                        [.795, .812, .825, .82, .805, .78, .75], 
                        [.82, .837, .848, .849, .835, .805, .78],
                        [.83, .845, .856, .86, .855, .84, .8], 
                        [.83, .848, .859, .869, .86, .852, .83], 
                        [.828, .845, .857, .869, .862, .855, .85], 
                        [.806, .83, .85, .86, .859, .857, .853], 
                        [.79, .8, .82, .835, .845, .848, .849]])


        self.m_dot_corr_ref = np.array([[10.45, 10.203, 9.784, 9.526, 9.144, 8.947, 8.615],
                                [13.315, 13.018, 12.525, 11.984, 11.455, 11.086, 10.914], 
                                [17.601, 17.204, 16.502, 15.8, 14.903, 14.179, 13.184],
                                [20.331, 19.983, 19.39, 18.492, 17.435, 16.293, 14.895],
                                [23.466, 23.092, 22.572, 21.807, 20.687, 19.3, 17.682],
                                [26.295, 26.091, 25.766, 25.28, 24.453, 23.26, 21.311],
                                [29.013, 28.747, 28.641, 28.412, 28.06, 27.098, 25.306],
                                [31.424, 31.379, 31.273, 31.103, 30.849, 30.484, 29.718],
                                [33.688, 33.606, 33.561, 33.513, 33.392, 33.258, 33.059],
                                [37.678, 37.621, 37.575, 37.598, 37.501, 37.415, 37.413]])
        
    def unscaled_dp(self):
        N_udp=9000, 
        m_udp=28.30
        
        PR_udp = self.map_interpolator("PR", scaled=False ,N=N_udp, x=m_udp)
        eta_udp = self.map_interpolator("eta", scaled=False ,N=N_udp, x=m_udp)
        N_perc_list = self.N_corr_ref/N_udp
        
        return N_perc_list, m_udp, PR_udp, eta_udp
    
    def scale_map(self, m_dp, PR_dp, eta_dp):
        N_perc_list, m_udp, PR_udp, eta_udp = self.unscaled_dp()
        
        f_m = m_dp/m_udp
        f_PR = (PR_dp-1)/(PR_udp-1)
        f_eta = eta_dp/eta_udp

        self.N_perc_list = N_perc_list
        self.m_scaled = f_m*self.m_dot_corr_ref
        self.PR_scaled = 1 + f_PR*(self.PR_comp-1)
        self.eta_scaled = f_eta*self.eta 
    
    def map_interpolator(self, map_type: "dict" , scaled :bool, N, x):
        """
        map_type = "PR" or "eta" depending on what you want to interpolate

        N = Number of corrected rpm

        x = Corrected mass flow rate both for "PR" and "eta" maps
        
        """
        if not scaled:
            N_list = self.N_corr_ref
            if map_type == "PR":
                x_list = self.m_dot_corr_ref
                y_list = self.PR_comp
            elif map_type == "eta":
                x_list = self.m_dot_corr_ref
                y_list = self.eta
        elif scaled:
            N_list = self.N_perc_list
            if map_type == "PR":
                x_list = self.m_scaled
                y_list = self.PR_scaled
            elif map_type == "eta":
                x_list = self.m_scaled
                y_list = self.eta_scaled
        
        
        # check
        if N < np.min(N_list) or N > np.max(N_list):
                raise Exception("NUMERO DI GIRI COMPRESSORE FUORI DAL RANGE DELLA MAPPA")

        for i in np.arange(len(N_list)-1):
            if N >= N_list[i] and N <= N_list[i+1]:
                #calcolare la % di distanza tra le due isocurve N
                perc = (N-N_list[i])/(N_list[i+1] - N_list[i])
                x_perc = x_list[i] + perc*(x_list[i+1] - x_list[i]) #è un vettore contenente le mdot dei punti a distanza %p
                y_perc = y_list[i] + perc*(y_list[i+1] - y_list[i]) #è un vettore contenente le beta dei punti a distanza %p
                break
        #faccio la spline passante per questi punti

        Df = pd.DataFrame({ "x_perc": x_perc,
                            "y_perc": y_perc})

        Df.sort_values(by=["x_perc"], inplace=True)

        x_perc = Df["x_perc"].values
        y_perc = Df["y_perc"].values

        spline_perc = PchipInterpolator(x_perc, y_perc, extrapolate=True)


        y = spline_perc(x)
        
                
        return y
                
    def dispmap(self, map_type ,scaled: bool ,x = 0 , y = 0, linetype="-*"):                   
        
        if not scaled:
            N_list = self.N_corr_ref
            if map_type == "PR":
                x_list = self.m_dot_corr_ref
                y_list = self.PR_comp
            elif map_type == "eta":
                x_list = self.m_dot_corr_ref
                y_list = self.eta
        elif scaled:
            N_list = self.N_perc_list
            if map_type == "PR":
                x_list = self.m_scaled
                y_list = self.PR_scaled
            elif map_type == "eta":
                x_list = self.m_scaled
                y_list = self.eta_scaled
        

        for i,k in enumerate(x_list):
            plt.plot(k, y_list[i])
            
        plt.plot(x,y,linetype)

    

        