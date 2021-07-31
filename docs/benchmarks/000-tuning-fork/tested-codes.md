# Tested Finite Element codes
```{contents} Table of Contents
:local:
:depth: 1
```
## CalculiX

CalculiX supports rigid body moves out of the box. Below there is an explanation of the input file.

```
** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/TET-0-5.inp # Path to mesh for ccx solver

** Material ++++++++++++++++++++++++++++++++++++++++++++++++

*Material, Name=Material-1	# Definition of material
*Density			# Definition of density
7.829E-09
*Elastic			# Definition of Young modulus and Poisson's ratio
207000, 0.33

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++
** # Assigning material and solid elements to the elements sets in mesh
*Solid section, Elset=Fork-El_Section, Material=Material-1	

** Steps +++++++++++++++++++++++++++++++++++++++++++++++++++
** # Definition of frequency step with 12 eigenmodes
*Step
*Frequency
12

** Field outputs +++++++++++++++++++++++++++++++++++++++++++
** # Commands responsible for saving results
*Node file
RF, U
*El file
S, E

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*End step
```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/00-Tuning-Fork/MODEL_CALCULIX)!

## Code_Aster

Unfortunately Code_Aster isn't ideal solver to obtain frequencies which are almost zero therefore the option BANDE was used to calculate frequencies in certain bandwidth. Below there is an explanation of the input file of Code_Aster.

```
DEBUT()


mesh = LIRE_MAILLAGE(FORMAT='MED',                          # Read the mesh
                     UNITE=20,
                     VERI_MAIL=_F())

model = AFFE_MODELE(AFFE=_F(MODELISATION=('3D', ),          # Assigning the element to the model
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=mesh)

mater = DEFI_MATERIAU(ELAS=_F(E=207000.0,                   # Defining the material
                              NU=0.33,
                              RHO=7.829e-09))

fieldmat = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),           # Assigning the material to the mesh
                                 TOUT='OUI'),
                         MAILLAGE=mesh,
                         MODELE=model)

ASSEMBLAGE(CHAM_MATER=fieldmat,                             # Setting the right matrixes for simulation
           MATR_ASSE=(_F(MATRICE=CO('MASS'),
                         OPTION='MASS_MECA'),
                      _F(MATRICE=CO('RIGI'),
                         OPTION='RIGI_MECA')),
           MODELE=model,
           NUME_DDL=CO('ndl'))




modes = CALC_MODES(CALC_FREQ=_F(FREQ=(100.0, 3000.0)),      # Setting the solver BANDE option between 100 and 3000 Hz.
                   MATR_MASS=MASS,
                   MATR_RIGI=RIGI,
                   OPTION='BANDE',
                   SOLVEUR_MODAL=_F(METHODE='TRI_DIAG',
                                    ),
                   TYPE_RESU='DYNAMIQUE')


IMPR_RESU(FORMAT='MED',                                     # Saving the result in 3D format
          RESU=_F(INFO_MAILLAGE='OUI',
                  RESULTAT=modes),
          UNITE=80)

IMPR_RESU(FORMAT='RESULTAT',                                # Saving the result in .dat file
          RESU=_F(RESULTAT=modes),
          UNITE=8)


FIN()

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/00-Tuning-Fork/MODEL_Code_Aster)!

## Elmer

Elmer supports rigid body modes out of the box. Below there is an explanation of solver input file.

```
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/QUAD-HEX-0-5" # Path to the mesh
  Include Path ""
  Results Directory "Results"     # Path to results directory
End

Simulation                        # Settings and constants for simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Solver Input File = case.sif
  Post File = case.ep
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

Body 1                            # Assigning the material and equations to the mesh
  Target Bodies(1) = 1
  Name = "Body 1"
  Equation = 1
  Material = 1
End

Solver 1                          # Solver settings
  Equation = Linear elasticity
  Procedure = "StressSolve" "StressSolver"
  Eigen System Select = Smallest magnitude
  Eigen System Values = 10
  Variable = -dofs 3 Displacement
  Eigen Analysis = True
  Exec Solver = Always
  Stabilize = True
  Bubbles = False
  Lumped Mass Matrix = False
  Optimize Bandwidth = True
  Linear System Convergence Tolerance = 1.0e-3
  Steady State Convergence Tolerance = 1.0e-5
  Nonlinear System Convergence Tolerance = 1.0e-7
  Nonlinear System Max Iterations = 1
  Nonlinear System Newton After Iterations = 3
  Nonlinear System Newton After Tolerance = 1.0e-3
  Nonlinear System Relaxation Factor = 1
  Linear System Solver = Direct
  Linear System Direct Method = MUMPS
End

Solver 2                          # Extracting the result to the .dat file
  Exec Solver = After Saving
  Equation ="Equation 1"
  Procedure = "SaveData" "SaveScalars"
  Filename = "QUAD-HEX-0-5.dat"
  Variable 1 = Displacement
  Save Eigenfrequencies = Logical True
End

Equation 1                        # Setting the active solvers
  Name = "Equation 1"
  Active Solvers(2) = 1 2
End

Material 1                        # Defining the material
  Name = "Steel"
  Mesh Poisson ratio = 0.33
  Youngs modulus = 207000
  Poisson ratio = 0.33
  Porosity Model = Always saturated
  Density = 7.829e-9
End

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/00-Tuning-Fork/MODEL_ElmerGUI)!

## MoFEM

Users who would like to check how the MoFEM model was created are advised to look into the MoFEM tutorials section [VEC-1: Eigen elastic](http://mofem.eng.gla.ac.uk/mofem/html/tutorial_eigen_elastic.html)

## GetFEM

```
"""

"""
###############################################################################

import time
import getfem as gf
import numpy as np
import scipy
from scipy import io
from scipy.sparse import linalg

###############################################################################
# Let us now define the different physical and numerical parameters of the problem.
#

rho = 7.829e-09  # Young Modulus (kg/mm^3)
E = 207000  # Young Modulus (N/mm^2)
nu = 0.33  # Poisson ratio
clambda = E * nu / ((1 + nu) * (1 - 2 * nu))  # First Lame coefficient (N/mm^2)
cmu = E / (2 * (1 + nu))  # Second Lame coefficient (N/mm^2)

###############################################################################
# Set the numerical parameter of each case.
#

elements_degrees = []
msh_file_names = []

# Linear-Tet 2.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-2-0.msh")

# Linear-Tet 1.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-1-0.msh")

# Linear-Tet 0.5mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-0-5.msh")

# Quad-Tet 2.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-2-0.msh")

# Quad-Tet 1.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-1-0.msh")

# Quad-Tet 0.5mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-0-5.msh")

# Linear-Hex 2.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-2-0.msh")

# Linear-Hex 1.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-1-0.msh")

# Linear-Hex 0.5mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-0-5.msh")

# Quad-Hex 2.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-2-0.msh")

# Quad-Hex 1.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-1-0.msh")

# Quad-Hex 0.5mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-0-5.msh")

t = time.process_time()

###############################################################################
# Importing the mesh from gmsh format.
#

meshs = []

for i, msh_file_name in enumerate(msh_file_names):
    mesh = gf.Mesh("import", "gmsh", msh_file_name)
    meshs.append(mesh)

print("Time for import mesh", time.process_time() - t)
t = time.process_time()

###############################################################################
# Definition of finite elements methods and integration method
#

mfus = []
mfds = []
mims = []

for elements_degree, mesh in zip(elements_degrees, meshs):

    mfu = gf.MeshFem(mesh, 3)
    mfu.set_classical_fem(elements_degree)
    mfus.append(mfu)

    mfd = gf.MeshFem(mesh, 1)
    mfd.set_classical_fem(elements_degree)
    mfds.append(mfd)

    mim = gf.MeshIm(mesh, elements_degree * 2)
    mims.append(mim)

###############################################################################
# We get the mass and stiffness matrices using asm function.
#

mass_matrixs = []
linear_elasticitys = []

for i, (mfu, mfd, mim) in enumerate(zip(mfus, mfds, mims)):

    mass_matrix = gf.asm_mass_matrix(mim, mfu, mfu)
    mass_matrix.scale(rho)
    mass_matrixs.append(mass_matrix)

    lambda_d = np.repeat(clambda, mfd.nbdof())
    mu_d = np.repeat(cmu, mfd.nbdof())
    linear_elasticity = gf.asm_linear_elasticity(mim, mfu, mfd, lambda_d, mu_d)
    linear_elasticitys.append(linear_elasticity)

    mass_matrix.save("hb", "M" + "{:02}".format(i) + ".hb")
    linear_elasticity.save("hb", "K" + "{:02}".format(i) + ".hb")

print("Time for assemble matrix", time.process_time() - t)
t = time.process_time()

###############################################################################
# Solve the eigenproblem.
#
# Compute the residual error for SciPy.
#
# :math:`Err=\frac{||(K-\lambda.M).\phi||_2}{||K.\phi||_2}`
#
# Convert Lambda values to Frequency values:
# :math:`freq = \frac{\sqrt(\lambda)}{2.\pi}`
#

for i, (mass_matrix, linear_elasticity, mfu) in enumerate(
    zip(mass_matrixs, linear_elasticitys, mfus)
):

    M = io.hb_read("M" + "{:02}".format(i) + ".hb")
    K = io.hb_read("K" + "{:02}".format(i) + ".hb")
    vals, vecs = linalg.eigsh(A=K, k=6, M=M, sigma=400.0, which="LA")

    omegas = np.sqrt(np.abs(vals))
    freqs = omegas / (2.0 * np.pi)

    nev = 6

    scipy_acc = np.zeros(nev)

    print(f"case{i}")

    for j in range(nev):
        lam = vals[j]  # j-th eigenvalue
        phi = vecs.T[j]  # j-th eigenshape

        kphi = K * phi.T  # K.Phi
        mphi = M * phi.T  # M.Phi

        kphi_nrm = np.linalg.norm(kphi, 2)  # Normalization scalar value

        mphi *= lam  # (K-\lambda.M).Phi
        kphi -= mphi

        scipy_acc[j] = np.linalg.norm(kphi, 2) / kphi_nrm  # compute the residual
        print(f"[{j}] : Freq = {freqs[j]:8.2f} Hz\t Residual = {scipy_acc[j]:.5}")

    np.savetxt("freqs" + "{:0=3}".format(i) + ".txt", freqs)
    mfu.export_to_vtk(
        "vecs" + "{:0=3}".format(i) + ".vtk",
        mfu,
        vecs[:, 0],
        "Mode_1",
        mfu,
        vecs[:, 1],
        "Mode_2",
        mfu,
        vecs[:, 2],
        "Mode_3",
        mfu,
        vecs[:, 3],
        "Mode_4",
        mfu,
        vecs[:, 4],
        "Mode_5",
        mfu,
        vecs[:, 5],
        "Mode_6",
    )

print("Time for solve eigen value problem", time.process_time() - t)
t = time.process_time()
```
