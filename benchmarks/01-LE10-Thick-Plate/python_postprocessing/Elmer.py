import numpy as np
import subprocess
import glob as gb
import shutil
import time
import os

#Function to convert mesh from .unv to Elmer format
def convert_from_unv_to_elmer(mesh_file):

    #Run ElmerGrid converter
    call = "ElmerGrid 8 2 " + mesh_file + " -removeunused -bulkorder -boundorder"
    print(call)
    subprocess.call([call],shell = True)

# Function changing input mesh inside the case.sif file
def change_case_sif (input_file, change_mesh):

    # Line needed to be changed in case.sif
    mesh_folder = '  Mesh DB "." "' + change_mesh + '"' +"\n"
    results_change = change_mesh.replace('Mesh/','Results/')		
    results_name = '  Results Directory "' + results_change + '"' "\n"

    # Read case.sif
    with open(input_file,"r") as case_sif_file:

    # Read all the lines of case.sif
        list_of_lines = case_sif_file.readlines()
        list_of_lines[2] = mesh_folder
        list_of_lines[4] = results_name

    with open(input_file, "w") as case_sif_file:
        case_sif_file.writelines(list_of_lines)

# Function which starts ElmerSolver
def run_elmer(input_file, directory):

    #os.mkdir("Results/" + directory)


    # Run the Elmer solver with ElmerSolver commnad
    call_elmer = "ElmerSolver " + input_file
    subprocess.call([call_elmer], shell = True)


# Check the meshes in Mesh folder
mesh_file_names = gb.glob("Mesh/*")

#Create results folder
os.mkdir("Results")
# Name of the input file for Elmer
elmer_input_file = ("case.sif")

for mesh_file_name in mesh_file_names:

    #convert_from_unv_to_elmer(mesh_file_name)
    #print(mesh_file_name)
    

    change_case_sif(elmer_input_file, mesh_file_name)
    run_elmer(elmer_input_file, mesh_file_name)

print ("All simualations are done!")
