import matplotlib.pyplot as plt

import numpy as np

if __name__ == "__main__":

    
    E = 210.0e3   

    sig_16mm = [
        0,
        320,
        357,
        366,
        541,
        541,
        ]

    eps_16mm = [
     0,
     sig_16mm[1]/E,
     sig_16mm[1]/E + 0.004,
     sig_16mm[1]/E + 0.0197,
     sig_16mm[1]/E + 0.1391,
     sig_16mm[1]/E + 0.1391*2
     ]    

    sig_40mm = [
        0,
        311,
        346.9,
        355.9,
        541.6,
        541.6,
        ]

    eps_40mm = [
     0,
     sig_16mm[1]/E,
     sig_16mm[1]/E + 0.004,
     sig_16mm[1]/E + 0.0197,
     sig_16mm[1]/E + 0.1391,
     sig_16mm[1]/E + 0.1391*2
     ]   
    
    plt.figure()
    
    plt.plot(eps_16mm, sig_16mm, marker="o", label="$t\leq16mm$")
    plt.plot(eps_40mm, sig_40mm, marker="o", label="$16mm<t\leq40mm$")
    
    plt.grid()
    plt.title("Engineering stress-strain")
    plt.xlabel("Strain (elastic+plastic) [-]")
    plt.ylabel("Stress [MPa]")
    plt.xticks(np.arange(0.0, 0.28, 0.02))
    plt.yticks(np.arange(0.0, 600, 50.0))
    
    plt.legend()
    plt.show()
    
    
    print("Values to implement in material definition for 16mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_16mm, sig_16mm):
        print(f"{strain:.4f} \t {stress}")

    print("Values to implement in material definition for 16-40 mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_40mm, sig_40mm):
        print(f"{strain:.4f} \t {stress}")
        
    