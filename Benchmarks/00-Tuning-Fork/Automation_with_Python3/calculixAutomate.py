import numpy as np
import subprocess 
import glob as gb
import shutil
import time
import os 	



def changeModelInp (inputFile, changeMesh):   # Function change input mesh inside the model.inp file 

    meshPath = "*INCLUDE, INPUT="+ changeMesh + "\n"     # Input mesh path
    ModelInp = open((inputFile + ".inp"),"r")            # Read model.np
    
    listofLines = ModelInp.readlines()                   # Read all the lines of model.inp
    listofLines[0] = meshPath                            # Change the first line of model.inp
          
    ModelInp = open((inputFile + ".inp"),"w")
    ModelInp.writelines(listofLines)
    ModelInp.close()
     
    
def runCalculix(inputFile, meshFilesInp):  # Function which starts ccx solver and copy results
    
    nameFilDir =  meshFilesInp.replace('.inp','')
    newNameFilDir =  nameFilDir.replace('Mesh/','')
    
    subprocess.run(["ccx_2.17_MT", inputFile])      # Run the CalculiX solver with ccx_2.17_MT commnad
    os.mkdir("Results/" + newNameFilDir)
    
    frdResultFile = inputFile + ".frd"             #Variables for copying/saving files
    datResultFile = inputFile + ".dat"
    
    frdNewName = newNameFilDir + ".frd"
    datNewName = newNameFilDir + ".dat"
    
    frdDir = "Results/" + newNameFilDir + "/" + frdNewName
    datDir = "Results/" + newNameFilDir + "/" + datNewName
       
    shutil.copyfile(frdResultFile, frdDir)      # Copy the results files
    shutil.copyfile(datResultFile, datDir)


    
os.mkdir("Results")   
meshFileNames = gb.glob("Mesh/*.inp") # Check the meshes in Mesh folder
ccxInputFile = ("model") # Name of the input inp file for CalculiX



for meshFileName in meshFileNames:
    
    print("\n"+meshFileName+"\n")
    changeModelInp(ccxInputFile, meshFileName)
    runCalculix(ccxInputFile, meshFileName)

print ("All the simualations are done!")







