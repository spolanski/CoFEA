import numpy as np
import subprocess
import glob as gb
import shutil
import time
import os


 # Function changing input mesh inside the RunCase_1.export file
def change_model_export (input_file, change_mesh):

    # Input RunCase_1.export
    mesh_path = "F libr /home/maciej/Documents/CoFEA/Eliptic_membrane/Model_Code_Aster/"+ change_mesh + " D 80" + "\n"

    # Read RunCase_1.export
    with open((input_file + ".export"),"r") as model_export:

    # Read all the lines of RunCase_1.export
        list_of_lines = model_export.readlines()
        list_of_lines[18] = mesh_path

    with open((input_file + ".export"),"w") as model_export:
    	model_export.writelines(list_of_lines)

# Function which starts Code_Aster and copy results
def run_code_aster(input_file, mesh_file_unv):

    name_fild_dir =  mesh_file_unv.replace('.unv','')
    new_name_fil_dir =  name_fild_dir.replace('Mesh/','')

    # Run the Code_Aster solver with as_run commnad
    input_full_name = input_file + ".export"
    subprocess.run(["as_run", input_full_name])
    os.mkdir("Results/" + new_name_fil_dir)

    #Variables for copying/saving files
    rmed_result_file = input_file + ".rmed"

    rmed_mew_name = new_name_fil_dir + ".rmed"

    rmed_dir = "Results/" + new_name_fil_dir + "/" + rmed_mew_name

    # Copy the results files
    shutil.copyfile(rmed_result_file, rmed_dir)

os.mkdir("Results")
# Check the meshes in Mesh folder
mesh_file_names = gb.glob("Mesh/*.unv")

# Name of the input inp file for Code_Aster
code_aster_input_file = ("RunCase_1")

for mesh_file_name in mesh_file_names:

    change_model_export(code_aster_input_file, mesh_file_name)
    run_code_aster(code_aster_input_file, mesh_file_name)

print ("All simualations are done!")
