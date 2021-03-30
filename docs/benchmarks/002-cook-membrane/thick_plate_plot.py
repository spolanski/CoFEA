import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.close('all')

def mesh_study():
    plot_title = 'Tetrahedral mesh comparison'
    file_name = 'tet-comparison_thick_plate.png'
    results = pd.read_csv('elipse_results.csv')

    lin_type = results['Mesh type'] == 'Linear-Tet'
    quad_type = results['Mesh type'] == 'Quad-Tet'
    mesh_type = results[lin_type | quad_type]
    zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
    labels = ["{} {}".format(i[0], i[1]) for i in zipped]
    ccx_values = mesh_type['Calculix'].tolist()
    code_aster_values = mesh_type['Code_Aster'].tolist()
    elmer_values = mesh_type['Elmer'].tolist()
    x = np.arange(len(labels))  # the label locations

    width = 0.2  # the width of the bars
    # plt.style.use('seaborn-white') 
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(x - 0.2, ccx_values, width, label='Calculix')
    ax.bar(x, code_aster_values, width, label='Code_Aster')
    ax.bar(x + 0.2, elmer_values, width, label='Elmer')

    target_value_x = [-1.5 * width, len(mesh_type) - 1 + 1.5 * width]
    ax.plot(target_value_x, 5.38 * np.ones_like(target_value_x), c='black',
            ls=('dashed'), label='Target 5.38 MPa')
    
    ax.set_ylabel('Absolute stress $\sigma_{yy}$ at point D [MPa]')
    ax.set_title(plot_title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(facecolor='white', framealpha=1)
    props = {"rotation" : 30}
    plt.setp(ax.get_xticklabels(), **props)
    fig.tight_layout()
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    fig.savefig(file_name)
    plt.show()

def code_comparison():
    plot_title = 'Code comparison'
    file_name = 'code-comparison.png'
    results = pd.read_csv('tuning_fork_results.csv')

    labels = [str(i) for i in range(1, 6)]
    ccx_values = results['Calculix'].tolist()
    code_aster_values = results['Code_Aster'].tolist()
    elmer_values = results['Elmer'].tolist()
    commercial = results['Commercial code'].tolist()
    x = np.arange(len(labels))  # the label locations

    width = 0.15  # the width of the bars
    # plt.style.use('seaborn-white') 
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(x - (1.5 * width), ccx_values, width, label='Calculix')
    ax.bar(x - (0.5 * width), code_aster_values, width, label='Code_Aster')
    ax.bar(x + (0.5 * width), elmer_values, width, label='Elmer')
    ax.bar(x + (1.5 * width), commercial, width, label='Commercial')

    # target_value_x = [-1.5 * width, len(results) - 1 + 1.5 * width]
    # ax.plot(target_value_x, 440.0 * np.ones_like(target_value_x), c='black',
    #         ls=('dashed'), label='Target 440Hz')

    ax.set_ylabel('Frequency [Hz]')
    ax.set_title(plot_title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(facecolor='white', framealpha=1)
    props = {"rotation" : 30}
    plt.setp(ax.get_xticklabels(), **props)
    fig.tight_layout()
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    fig.savefig(file_name)
    plt.show()
    
if __name__ == "__main__":
    mesh_study()
    #code_comparison()
