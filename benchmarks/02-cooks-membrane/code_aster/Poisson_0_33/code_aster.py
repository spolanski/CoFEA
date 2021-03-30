import numpy as np
import subprocess
import glob as gb
import shutil
import time
import os
from collections import OrderedDict
import pandas as pd
def run_study():
    mesh_file_names = gb.glob("Mesh/*.unv")

    # Name of the input inp file for Code_Aster
    code_aster_input_file = ("study")

    results = []
    for mesh_dir_name in mesh_file_names:
        mesh_type = mesh_dir_name.split('/')[-1].split('.')[0]
        with open('study.export', 'r') as f:
            export_file = f.read().replace('_tochange_', mesh_type).replace('_meshtype_', mesh_type)
        # print(export_file)
        new_dir = os.getcwd() + "/Results/" + mesh_type
        os.makedirs(new_dir)
        shutil.copyfile(os.getcwd() + '/' + mesh_dir_name,
                        os.getcwd() + '/Results/{0}/{0}.unv'.format(mesh_type))
        shutil.copyfile(os.getcwd() + '/' + 'study.comm',
                        os.getcwd() + '/Results/{0}/study.comm'.format(mesh_type))
        with open(new_dir + '/' + mesh_type + '.export', 'w') as f:
            f.write(export_file)
        print("as_run" + os.getcwd() + '/Results/{0}/{0}.export'.format(mesh_type))
        cmd = "/home/spolanski/salome_meca/V2020.0.1_universal_universal/tools/Code_aster_frontend-202001/bin/as_run " + os.getcwd() + '/Results/{0}/{0}.export'.format(mesh_type)
        subprocess.call(cmd, shell=True)
        try:
            with open(os.getcwd() + '/Results/{0}/table.txt'.format(mesh_type), 'r') as f:
                dy = f.read().split('\n')[-3].split(' ')[-1]
                size, shape_func, elem_type = mesh_type.split('_')
                results.append(("{}-{}".format(shape_func, elem_type), size,
                                float(dy)))
        except:
            size, shape_func, elem_type = mesh_type.split('_')
            results.append(("{}-{}".format(shape_func, elem_type), size, 0.0))

    data_frame = pd.DataFrame({'Mesh type': [i[0] for i in results],
                               'Size': [i[1] for i in results],
                               'Code_Aster': [i[2] for i in results]})
    data_frame.sort_values(by=['Mesh type', 'Size'], inplace=True)
    data_frame.to_csv('poisson_0_33.csv')
    print(data_frame)

run_study()
