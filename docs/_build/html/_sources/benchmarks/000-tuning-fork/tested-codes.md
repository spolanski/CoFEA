# Tested Finite Element codes
## CalculiX

CalculiX supports rigid body moves out of the box. Below there is an explanation of the input file.

```
** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/cofea-coarse-quad-hex.inp  # Path to mesh for ccx solver

** Material ++++++++++++++++++++++++++++++++++++++++++++++++

*MATERIAL, NAME=Steel                                    # Defining a material
    *DENSITY
        7850                                             # Defining a density
    *ELASTIC,
        2.1e11, 0.3                                      # Defining Young modulus and Poisson's ratio

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++

*SOLID SECTION, ELSET=PART-1-1-EL-EALL, MATERIAL=Steel   # Assigning material and solid elements
                                                         # to the elements sets in mesh
** Steps +++++++++++++++++++++++++++++++++++++++++++++++++++

*STEP                                                    # Begin of analysis
    *STATIC, SOLVER=SPOOLES                              # Selection of elastic analysis

** Field outputs +++++++++++++++++++++++++++++++++++++++++++

    *EL FILE                                             # Commands responsible for saving results
        E, S
    *NODE FILE
        U
    *EL PRINT,ELSET=EL-EOUT
        S

** Boundary conditions +++++++++++++++++++++++++++++++++++++

    *BOUNDARY,                                           # Applying translation = 0 on desired nodes
        N-AB,1,1,0
    *BOUNDARY
        N-DC,2,2,0
    *BOUNDARY
        N-BC,1,1,0
	      N-BC,2,2,0
    *BOUNDARY
        N-MID,3,3,0

** Boundary conditions(adding pressure) ++++++++++++++++++++

    *DLOAD,
    *INCLUDE, INPUT=Pressure/cofea-coarse-quad-hex.dlo

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*End step                      # End on analysis

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
