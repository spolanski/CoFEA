import matplotlib.pyplot as plt
import numpy as np

digitized_values = np.loadtxt(
    "beam_strain_profile_digitization.csv",
    skiprows=6, 
    delimiter=",",
    )

plt.figure()
plt.xlabel("Maximum principal plastic strain [-]")
plt.ylabel("Web height [mm]")
plt.plot(digitized_values[:,0], digitized_values[:,1])
plt.yticks(np.arange(0,500+20, 20))
plt.xticks(np.arange(0, 0.05+0.005, 0.005))
plt.grid()
plt.show()