from B_1_1_cantilever_beam_centroid import *

# Axial force [kN]
N = 500.0e3
# Transverse vertical force [kN]
P = -75.0e3
# Moment of force [kN*mm]
M = -225.0e3
# Cantilever's length [mm]
L = 3000.0 

sigma_upper_1 = abs(N)/A 
sigma_upper_2 = M / Wy_upper  
sigma_upper_3 = (abs(P)*L)/Wy_upper 

print(f"sigma_upper_1 : {sigma_upper_1}")
print(f"sigma_upper_2 : {sigma_upper_2}")
print(f"sigma_upper_3 : {sigma_upper_3}")
print(f"sigma_upper_1+sigma_upper_2+sigma_upper_3 : {sigma_upper_1+sigma_upper_2+sigma_upper_3}")

sigma_lower_1 = abs(N)/A 
sigma_lower_2 = M / Wy_lower
sigma_lower_3 = (abs(P)*L)/Wy_lower

print(f"sigma_lower_1 : {sigma_lower_1}")
print(f"sigma_lower_2 : {sigma_lower_2}")
print(f"sigma_lower_3 : {sigma_lower_3}")