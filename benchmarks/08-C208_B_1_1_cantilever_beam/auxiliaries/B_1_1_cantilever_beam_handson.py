from B_1_1_cantilever_beam_centroid import *

# N Axial force [kN]
N = 500.0e3
# P = -0.15*N Transverse vertical force [kN]
P = -75.0e3
# M = -0.45*N*1m Moment of force [kN*mm]
M = -225.0e3 * 1000.0
# Cantilever's length [mm]
L = 3000.0 

## Normal principal stress in the upper part of the web
# from axial force N
sigma_upper_1 = abs(N)/A 
# from moment M
sigma_upper_2 = M / Wy_upper  
# from transverse force P
sigma_upper_3 = (abs(P)*L)/Wy_upper 

print(f"sigma_upper_1 : {sigma_upper_1}")
print(f"sigma_upper_2 : {sigma_upper_2}")
print(f"sigma_upper_3 : {sigma_upper_3}")
print(f"sigma_upper_1+sigma_upper_2+sigma_upper_3 : {sigma_upper_1+sigma_upper_2+sigma_upper_3}")

## Normal principal stress in the lower part of the flange
# from axial force N
sigma_lower_1 = abs(N)/A 
# from moment M
sigma_lower_2 = M / Wy_lower
# from transverse force P
sigma_lower_3 = (abs(P)*L)/Wy_lower

print(f"sigma_lower_1 : {sigma_lower_1}")
print(f"sigma_lower_2 : {sigma_lower_2}")
print(f"sigma_lower_3 : {sigma_lower_3}")