# Tested Finite Element codes

## CalculiX

```
** # Material - material definition in Pa, m
*Material, Name=Material-1
*Elastic
22770000, 0.35

** # Section - shell thickness definition
*Shell section, Elset=S4R, Material=Material-1, Offset=0
0.0508

** # Step-1 - Static step definition
*Step
*Static

** # Boundary conditions definition
** # Name: Displacement fix
*Boundary, Fixed
fixedge, 1, 1
fixedge, 2, 2
fixedge, 3, 3
```

## Code_Aster

```
# Read mesh from UNV file
mesh = LIRE_MAILLAGE(FORMAT='IDEAS',
                     UNITE=2)

# Define quadratic element type
m_quad = CREA_MAILLAGE(MAILLAGE=mesh,
                       MODI_MAILLE=_F(OPTION='QUAD8_9',
                                      PREF_NOEUD='NS',
                                      TOUT='OUI'))

# Create shell definition for quadratic elements
pallet = AFFE_MODELE(AFFE=_F(MODELISATION=('COQUE_3D', ),
                             PHENOMENE='MECANIQUE',
                             TOUT='OUI'),
                     MAILLAGE=m_quad)

# Define shell thickness
elemprop = AFFE_CARA_ELEM(COQUE=_F(EPAIS=0.0508,
                                   GROUP_MA=('main', )),
                          MODELE=pallet)

# Define type of element section
# Notice that mesh, not m_quad variable is used
Postpro = AFFE_MODELE(AFFE=_F(MODELISATION=('3D', ),
                              PHENOMENE='MECANIQUE',
                              TOUT='OUI'),
                      MAILLAGE=mesh)

# Define material properties
mater = DEFI_MATERIAU(ELAS=_F(E=22770000.0,
                              NU=0.35))

# Assign material to the elements
materfl = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),
                                TOUT='OUI'),
                        MODELE=pallet)

# Define boundary conditions
mecabc = AFFE_CHAR_MECA(DDL_IMPO=_F(DRX=0.0,
                                    DRY=0.0,
                                    DRZ=0.0,
                                    DX=0.0,
                                    DY=0.0,
                                    DZ=0.0,
                                    GROUP_MA=('fixedge', )),
                        MODELE=pallet)

```
## Elmer

```
# Load mesh and define the path for the path
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/L_VF_T"
  Include Path ""
  Results Directory "Results/L_VF_T"
End

# Define type of simulation, CSYS and output file
Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Solver Input File = case.sif
  Post File = case.vtu
End

# Define constants
Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.670374419e-08
  Permittivity of Vacuum = 8.85418781e-12
  Permeability of Vacuum = 1.25663706e-6
  Boltzmann Constant = 1.380649e-23
  Unit Charge = 1.6021766e-19
End

# Assign material and section definition
Body 1
  Target Bodies(1) = 1
  Name = "Body 1"
  Equation = 1
  Material = 1
End

# Define shell solver definition
Solver 1
  Equation = "Shell equations"
  Procedure = "ShellSolver" "ShellSolver"
  Large Deflection = False
  Linear System Solver = Direct
  Linear System Preconditioning = ILU0
  Linear System Row Equilibration = Logical True
  Linear System Max Iterations = 1000
  Linear System Convergence Tolerance = 1e-8
  Linear System Direct Method = Umfpack
  Linear System GCR Restart = 300
  Linear System Abort Not Converged = False
  Steady State Convergence Tolerance = 1e-09
End

# Define solver to output displacement into the file
Solver 2 
  Equation = SaveScalars
  Procedure = "SaveData" "SaveScalars"
  Filename = results.dat
  Variable 1 = String u
  Operator 1 = String 3
  Save Points = 6
End

# Define shell behaviour
Equation 1
  Name = "ShellSolver"
  Active Solvers(1) = 1
End

# Define material properties
Material 1
  Name = "Material 1"
  Shell Thickness = 0.0508
  Poisson ratio = 0.35
  Youngs modulus = 22.77e6
End

# Define encastre conditions
Boundary Condition 1
  Target Boundaries(1) = 1 
  Name = "Fix"
  U 2 = 0
  U 3 = 0
  U 1 = 0
  DNU 3 = 0
  DNU 2 = 0
  DNU 1 = 0
End

# Define distributed load
Boundary Condition 2
  Target Boundaries(1) = 2 
  Name = "Force"
  Resultant Force 3 = Real 8.7563
End
```
