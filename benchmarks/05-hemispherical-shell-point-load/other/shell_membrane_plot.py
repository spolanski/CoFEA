import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.close('all')

def mesh_study():
    plot_title = 'Quadrilateral mesh comparison'
    file_name = 'quad-comparison_eliptic_membrane.png'
    results = pd.read_csv('shell_membrane.csv')

    lin_type = results['Mesh type'] == 'Linear-Quad'
    quad_type = results['Mesh type'] == 'Quad-Quad'
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
    ax.plot(target_value_x, 0.185 * np.ones_like(target_value_x), c='black',
            ls=('dashed'), label='Target 0.185m')

    ax.set_ylabel('Displacement $u_{x}$ at point A [m]')
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
    
