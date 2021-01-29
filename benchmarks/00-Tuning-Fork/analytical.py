import numpy as np
L = 66.74e-3 + 4.2e-3 # length of the prongs [m]
E = 2.07e11 # Young's modulus of steel [Pa]
rho = 7829.0 # density of steel [kg/m^3]
a = 3.0e-3 # width of the prong [m]
I = (a**4.0)/12.0
A = a*a


f1 = ((1.875**2.0) / (2.0 * np.pi * (L**2.0))) * np.sqrt((E * I) / (rho * A))
print(f1)
print('{:.4f}'.format(L))
print((abs(495.0 - 440.0)/440.0)*100.0)