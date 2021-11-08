import matplotlib.pyplot as plt

import numpy as np

if __name__ == "__main__":

    
    E = 210.0e3   

    sig_16mm_true = [
        0,
        320,
        357,
        366,
        541,
        541,
        ]

    eps_16mm_true = [
     0,
     sig_16mm_true[1]/E,
     sig_16mm_true[1]/E + 0.004,
     sig_16mm_true[1]/E + 0.0197,
     sig_16mm_true[1]/E + 0.1391,
     sig_16mm_true[1]/E + 0.1391*2
     ]    

    sig_40mm_true = [
        0,
        311,
        346.9,
        355.9,
        541.6,
        541.6,
        ]

    eps_40mm_true = [
     0,
     sig_16mm_true[1]/E,
     sig_16mm_true[1]/E + 0.004,
     sig_16mm_true[1]/E + 0.0197,
     sig_16mm_true[1]/E + 0.1391,
     sig_16mm_true[1]/E + 0.1391*2
     ]   



    sig_16mm_engi = [
        0,
        319.5,
        355,
        358.4,
        470,
        470,
        ]

    eps_16mm_engi = [
     0,
     sig_16mm_true[1]/E,
     sig_16mm_true[1]/E + 0.004,
     sig_16mm_true[1]/E + 0.02,
     sig_16mm_true[1]/E + 0.15,
     sig_16mm_true[1]/E + 0.15*2
     ]    

    sig_40mm_engi = [
        0,
        310.5,
        345,
        348.4,
        470,
        470,
        ]

    eps_40mm_engi = [
     0,
     sig_16mm_true[1]/E,
     sig_16mm_true[1]/E + 0.004,
     sig_16mm_true[1]/E + 0.02,
     sig_16mm_true[1]/E + 0.15,
     sig_16mm_true[1]/E + 0.15*2
     ]   





    
    plt.figure()
    
    plt.plot(eps_16mm_true, sig_16mm_true, marker="o", label="$t\leq16mm$ True stress-strain")
    plt.plot(eps_40mm_true, sig_40mm_true, marker="o", label="$16mm<t\leq40mm$ True stress-strain")

    plt.plot(eps_16mm_engi, sig_16mm_engi, marker="o", linestyle="-.", label="$t\leq16mm$ Engineering stress-strain")
    plt.plot(eps_40mm_engi, sig_40mm_engi, marker="o", linestyle="-.", label="$16mm<t\leq40mm$ Engineering stress-strain")
    
    plt.grid()
    plt.title("Stress-strain")
    plt.xlabel("Strain (elastic+plastic) [-]")
    plt.ylabel("Stress [MPa]")
    plt.xticks(np.arange(0.0, 0.28, 0.02))
    plt.yticks(np.arange(0.0, 600, 50.0))
    
    plt.legend()
    plt.show()
    
    print("### Material definition based on true stress-strain ###")
    print("Values to implement in material definition for 16mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_16mm_true, sig_16mm_true):
        print(f"{strain:.4f} \t {stress}")

    print("Values to implement in material definition for 16-40 mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_40mm_true, sig_40mm_true):
        print(f"{strain:.4f} \t {stress}")
   
    print("### Material definition based on engineering stress-strain ###")
    print("Values to implement in material definition for 16mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_16mm_engi, sig_16mm_engi):
        print(f"{strain:.4f} \t {stress}")

    print("Values to implement in material definition for 16-40 mm thickness S355:")
    print("strain \t stress")
    for strain, stress in zip(eps_40mm_engi, sig_40mm_engi):
        print(f"{strain:.4f} \t {stress}")
    