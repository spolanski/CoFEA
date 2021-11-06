import matplotlib.pyplot as plt
import numpy as np


def load_resu_epeq(path):

    # Load .resu file, and use columns with coordinate and principal plastic strain
    array = np.loadtxt(
        path,
        skiprows=5, 
        delimiter=" ",
        usecols = [31, 39]
        )    
    
    # Reorient coordinate column
    array[:,0] = array[:,0][::-1]
    
    return array

if __name__ == "__main__":
        
    # Load values digitized from standard DNV C208 
    c208_res = np.loadtxt(
        "digitized_plastic_curve/beam_strain_profile_digitization.csv",
        skiprows=6, 
        delimiter=",",
        )
    # Linearized values from DNV C208
    c208_res_lin = np.array(
        [[0.0, -0.01],
        [480.0, 0.039]]
        )

    # Load results obtained in Code Aster, based on engineering stres-strain material curve    
    c_a_engi = load_resu_epeq("../results/C_A_epeq_elno_PRIN_3_engi.resu")
    # Linearize values
    c_a_engi_lin_coefs = np.polyfit(c_a_engi[:,0], c_a_engi[:,1],1)
    c_a_engi_lin = np.polyval(c_a_engi_lin_coefs, c_a_engi[:,0])
    
    # Load results obtained in Code Aster, based on true stres-strain material curve    
    c_a_true = load_resu_epeq("../results/C_A_epeq_elno_PRIN_3_true.resu")
    # Linearize values
    c_a_true_lin_coefs = np.polyfit(c_a_true[:,0], c_a_true[:,1],1)
    c_a_true_lin = np.polyval(c_a_true_lin_coefs, c_a_true[:,0])

    # Plot results
    plt.figure()
    plt.xlabel("Maximum principal plastic strain [-]")
    plt.ylabel("Web height [mm]")
    
    plt.plot(c208_res[:,0], c208_res[:,1], color="blue", label="DNV C208 standard, 489kN")
    plt.plot(c208_res_lin[:,1], c208_res_lin[:,0], color="blue", linestyle ="-.", label="DNV C208 standard - linearized, 489kN")
    
    plt.plot(c_a_engi[:,1], c_a_engi[:,0], color="orange", label ="Code_Aster, engineering stress-strain input, 489kN")
    plt.plot(c_a_engi_lin, c_a_engi[:,0], color="orange", linestyle ="-.", label ="Code_Aster, engineering stress-strain input, linearized, 489kN")
    
    plt.plot(c_a_true[:,1], c_a_true[:,0], color="grey", label ="Code_Aster, true stress-strain input, 489kN")
    plt.plot(c_a_true_lin, c_a_true[:,0], color="grey", linestyle ="-.", label ="Code_Aster, true stress-strain input, linearized, 489kN")
    
    plt.yticks(np.arange(0,500+20, 20))
    plt.xticks(np.arange(-0.02, 0.05+0.005, 0.005))
    plt.legend(loc=4)
    plt.grid()
    plt.show()