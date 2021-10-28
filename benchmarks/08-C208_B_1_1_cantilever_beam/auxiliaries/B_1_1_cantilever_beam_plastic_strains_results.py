import matplotlib.pyplot as plt
import numpy as np

digitized_values = np.loadtxt(
    "digitized_plastic_curve/beam_strain_profile_digitization.csv",
    skiprows=6, 
    delimiter=",",
    )


c_a_values = np.loadtxt(
    "../results/C_A_epeq_elno_PRIN_3.resu",
    skiprows=5, 
    delimiter=" ",
    usecols = [29, 31, 39]
    )

c_a_values_475kN  = c_a_values[:int(len(c_a_values)/2)]
c_a_values_500kN  = c_a_values[int(len(c_a_values)/2):]


print(c_a_values)

plt.figure()
plt.xlabel("Maximum principal plastic strain [-]")
plt.ylabel("Web height [mm]")
plt.plot(digitized_values[:,0], digitized_values[:,1], label="DNV C208 standard, 489kN")

plt.plot(c_a_values_475kN[:,2][::-1], c_a_values_475kN[:,1], label ="Code_Aster, 475kN")
plt.plot(c_a_values_500kN[:,2][::-1], c_a_values_500kN[:,1], label ="Code_Aster, 500kN")
plt.yticks(np.arange(0,500+20, 20))
plt.xticks(np.arange(0, 0.05+0.005, 0.005))
plt.legend()
plt.grid()
plt.show()