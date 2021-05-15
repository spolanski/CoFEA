import numpy as np
import subprocess
import glob as gb
import shutil
import time
import os

#Function to convert mesh from .unv to Elmer format
def convert_from_inp_to_elmer(mesh_file):

    #Run ElmerGrid converter
    call = "ElmerGrid 8 2 " + mesh_file
    print(call)
    subprocess.call([call],shell = True)

# Function changing input mesh inside the case.sif file
def change_case_sif (input_file, change_mesh):

    # Line needed to be changed in case.sif
    mesh_folder = '  Mesh DB "." "Mesh/' + change_mesh + '"' +"\n"
    results_name = '  Filename = "' + change_mesh + '.dat"' +"\n"

    # Read case.sif
    with open(input_file,"r") as case_sif_file:

    # Read all the lines of case.sif
        list_of_lines = case_sif_file.readlines()
        list_of_lines[2] = mesh_folder
        list_of_lines[62] = results_name

    with open(input_file, "w") as case_sif_file:
        case_sif_file.writelines(list_of_lines)

# Function which starts ElmerSolver
def run_elmer(input_file, directory):

    os.mkdir("Results/" + directory)


    # Run the Elmer solver with ElmerSolver command
    call_elmer = "ElmerSolver " + input_file
    subprocess.call([call_elmer], shell = True)

    dat_result_file = "Results/" + directory + ".dat"
    dat_names_result_file = "Results/" + directory + ".dat.names"

    new_dat_result_file = "Results/"+ directory + "/" + directory + ".dat"
    new_dat_names_result_file = "Results/"+ directory + "/" + directory + ".dat.names"


    # Copy the results files
    shutil.move(dat_result_file, new_dat_result_file)
    shutil.move(dat_names_result_file, new_dat_names_result_file)




# Check the meshes in Mesh folder
mesh_file_names = os.listdir("Mesh/")

#Create results folder
os.mkdir("Results")
# Name of the input file for Elmer
elmer_input_file = ("case.sif")

for mesh_file_name in mesh_file_names:

    #convert_from_inp_to_elmer(mesh_file_name)
    print(mesh_file_name)
    #mesh_file_name = mesh_file_name.replace('.unv', "")
    mesh_file_name = mesh_file_name.replace('Mesh/','')

    change_case_sif(elmer_input_file, mesh_file_name)
    run_elmer(elmer_input_file, mesh_file_name)

print ("All the simualations are done!")
