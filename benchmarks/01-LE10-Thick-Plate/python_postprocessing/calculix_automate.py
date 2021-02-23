import numpy as np
import subprocess
import glob as gb
import shutil
import time
import os
import logging
import ccx2paraview




 # Function changing input mesh inside the model.inp file
def change_model_inp (input_file, change_mesh):

    # Input mesh path
    mesh_path = "*INCLUDE, INPUT="+ change_mesh + "\n"

    # Pressure load path
    press_path = change_mesh.replace('Mesh/','Pressure/')
    press_name = press_path.replace('.inp','.dlo')
    press_load_path = "    *INCLUDE, INPUT=" + press_name + "\n"

    # Read model.inp
    with open((input_file + ".inp"),"r") as model_inp:

    # Read all the lines of model.inp
        list_of_lines = model_inp.readlines()
        list_of_lines[0] = mesh_path
        list_of_lines[25] = press_load_path

    with open((input_file + ".inp"),"w") as model_inp:
    	model_inp.writelines(list_of_lines)

# Function which starts ccx solver and copy results
def run_calculix(input_file, mesh_files_inp):

    name_fild_dir =  mesh_files_inp.replace('.inp','')
    new_name_fil_dir =  name_fild_dir.replace('Mesh/','')

    # Run the CalculiX solver with ccx_2.17_MT commnad
    subprocess.run(["ccx_2.17_MT", input_file])
    os.mkdir("Results/" + new_name_fil_dir)

    #Variables for copying/saving files
    frd_result_file = input_file + ".frd"
    dat_result_file = input_file + ".dat"
    vtu_result_file = input_file + ".vtu"

    #convert .frd to .vtu
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    conversion = ccx2paraview.Converter(frd_result_file, ['vtu'])
    conversion.run()

    frd_new_name = new_name_fil_dir + ".frd"
    dat_new_name = new_name_fil_dir + ".dat"
    vtu_new_name = new_name_fil_dir + ".vtu"

    frd_dir = "Results/" + new_name_fil_dir + "/" + frd_new_name
    dat_dir = "Results/" + new_name_fil_dir + "/" + dat_new_name
    vtu_dir = "Results/" + new_name_fil_dir + "/" + vtu_new_name

    # Copy the results files
    shutil.copyfile(frd_result_file, frd_dir)
    shutil.copyfile(dat_result_file, dat_dir)
    shutil.copyfile(vtu_result_file, vtu_dir)

os.mkdir("Results")
# Check the meshes in Mesh folder
mesh_file_names = gb.glob("Mesh/*.inp")

# Name of the input inp file for CalculiX
ccx_input_file = ("model")

for mesh_file_name in mesh_file_names:

    change_model_inp(ccx_input_file, mesh_file_name)
    run_calculix(ccx_input_file, mesh_file_name)

print ("All simualations are done!")
