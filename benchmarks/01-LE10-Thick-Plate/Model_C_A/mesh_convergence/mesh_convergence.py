#!/usr/bin/env python
"""
Script connects preparing meshes with various mesh parameters.

What is important before running the script!:
1. Define your own directory to salome application i.e: SALOME_PATH
2. Define your directory where meshes will be updated i.e. EXPORT_MESH_PATH
3. Define your directiories in mesh_convergence.export file
4. Define your RESULT_PATH in mesh_convergence.comm file - there will be
    text file with SIYY value in point D
That's all! Script was written and checked in accordance with Salome-Meca 2019.0.3
and Code_Aster v14.4

MESH_MULTPILIERS is the list of iterative parameter. With parameter 1,
the vertical lines are divided to 2 segments, radial lines by 2,
circumferential by 3. Consecutive numbers of mesh_multpliers increase the
division by multiplying abovementioned numbers. MESH_MULTIPLIERS must include
integeres only

"""
import subprocess
import os

if __name__ == "__main__":
    SALOME_PATH = "/home/filon/salome_software/appli_V2019.0.3_universal/salome"
    EXPORT_MESH_PATH = "/home/filon/salome_projects/repo/CoFEA/Benchmarks/01-LE10-Thick-Plate/Model_C_A/mesh_convergence/"
    PREPARE_MESH_PATH = EXPORT_MESH_PATH + "salome_prepare_mesh.py"

    REGULAR_MESH = False
    LINEAR_ELEMENTS = True
    MESH_MULTPILIERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]

    for mesh_multiplier in MESH_MULTPILIERS:
        input_string_to_prepare_mesh = f"{SALOME_PATH} --terminal {PREPARE_MESH_PATH} args:{EXPORT_MESH_PATH},args:{mesh_multiplier},args:{REGULAR_MESH},args:{LINEAR_ELEMENTS}"
        subprocess.run(input_string_to_prepare_mesh , shell=True)

        input_string_to_solve = f"{SALOME_PATH} shell -- as_run {EXPORT_MESH_PATH}mesh_convergence.export"
        subprocess.run(input_string_to_solve, shell=True)
