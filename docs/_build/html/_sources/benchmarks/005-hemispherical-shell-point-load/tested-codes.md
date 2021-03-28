# Tested Finite Element codes
## CalculiX

CalculiX supports elastic simulation. Below there is an explanation of the input file.

```
** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/fine-lin-hex.inp		# Path to mesh for ccx solver

** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*MATERIAL, NAME=MAT				# Defining a material
*ELASTIC,
68.25e9, 0.3					# Defining Young modulus and Poisson's ratio

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++

*SHELL SECTION, ELSET=Shell, MATERIAL=MAT,OFFSET= # Assigning material and plane stress elements
 0.04, 	# to the elements sets in mesh and adding thickness

** Steps +++++++++++++++++++++++++++++++++++++++++++++++++++

*STEP						# Begin of analysis
*STATIC, SOLVER=SPOOLES				# Selection of elastic analysis

** Field outputs +++++++++++++++++++++++++++++++++++++++++++

*EL FILE					# Commands responsible for saving results
E, S
*NODE FILE
U

** Boundary conditions +++++++++++++++++++++++++++++++++++++

*BOUNDARY,					# Applying translation = 0 on desired nodes
E,1,3,0
AE,2,2,0
AE,4,4,0
AE,6,6,0
CE,1,1,0
CE,5,6,0

** Boundary conditions(adding force on nodes) ++++++++++++++++++++

*CLOAD
A,1,2000
C,2,-2000

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*END STEP					# End on analysis


```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/05-hemispherical-shell-point-load/Model_CalculiX)!


## Code_Aster

Code_Aster supports elastic simulation. Below there is an explanation of the input file.


```
DEBUT(LANG='EN')

mesh = LIRE_MAILLAGE(identifier='0:1',                   	 # Reading the mesh
                     FORMAT='IDEAS',
                     UNITE=80)


Quad8 = CREA_MAILLAGE(LINE_QUAD=_F(PREF_NOEUD='NQ',
                                   TOUT='OUI'),
                      MAILLAGE=mesh)

Quad9 = CREA_MAILLAGE(MAILLAGE=Quad8,                     	# Transforming QUAD8 to QUAD9
                      MODI_MAILLE=_F(OPTION='QUAD8_9',
                                     PREF_NOEUD='NS',
                                     TOUT='OUI'))

model = AFFE_MODELE(AFFE=_F(MODELISATION=('COQUE_3D', ),  	# Assigning the elements
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=Quad9)

elemprop = AFFE_CARA_ELEM(COQUE=_F(EPAIS=0.04,            	# Assigning the thickness
                                   GROUP_MA=('Shell', )),
                          MODELE=model)

mater = DEFI_MATERIAU(ELAS=_F(E=68250000000.0,            	# Defining the material   
                              NU=0.3))

fieldmat = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),         	# Assigning material to model
                                 TOUT='OUI'),
                         MAILLAGE=Quad9,
                         MODELE=model)

BC = AFFE_CHAR_MECA(DDL_IMPO=(_F(DX=0.0,                   	# Applying the boundary condition
                                 DY=0.0,
                                 DZ=0.0,
                                 GROUP_NO=('E', )),
                              _F(DRX=0.0,
                                 DRZ=0.0,
                                 DY=0.0,
                                 GROUP_NO=('AE', )),
                              _F(DRY=0.0,
                                 DRZ=0.0,
                                 DX=0.0,
                                 GROUP_NO=('CE', ))),
                    MODELE=model)

load0 = AFFE_CHAR_MECA(FORCE_NODALE=(_F(FX=2000.0,          	# Applying forces
                                        GROUP_NO=('A', )),
                                     _F(FY=-2000.0,
                                        GROUP_NO=('C', ))),
                       MODELE=model)

reslin = MECA_STATIQUE(CARA_ELEM=elemprop,			              # Defining results of simulation
                       CHAM_MATER=fieldmat,
                       EXCIT=(_F(CHARGE=BC),
                              _F(CHARGE=load0)),
                       MODELE=model)

IMPR_RESU(FORMAT='RESULTAT',					                        # Saving the results
          RESU=_F(RESULTAT=reslin,
		  GROUP_NO=('A',)),
          UNITE=8)

FIN()

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/05-hemispherical-shell-point-load//Model_Code_Aster)!

## Elmer

Elmer supports elastic simulations out of the box. Below there is an explanation of solver input file.

```
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "."				# Path to the mesh
  Include Path ""
  Results Directory ""				# Path to results directory
End

Simulation					# Settings and constants for simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Solver Input File = case.sif
  Post File = case.vtu
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

Body 1						# Assigning the material and equations to the mesh
  Target Bodies(1) = 6
  Name = "Body 1"
  Equation = 1
  Material = 1
End

Solver 1  # Solver calculating normal vectors
  Equation = "Director field"
  Procedure = "SphereNormalSolver" "NormalSolver"
  Exec Solver = "Before Simulation"
  Normals Result Variable = String "Director"
  Exported Variable 1 = Director[Director:3]
  Linear System Solver = "Iterative"
  Linear System Iterative Method = "IDRS"
  Linear System Preconditioning = None
  Linear System Residual Output = 10
  Linear System Max Iterations = 500
  Linear System Convergence Tolerance = 1.0e-10
End

Solver 2					# Solver shell settings
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

Equation 1					# Setting active solvers
  Name = "Equation 1"
  Active Solvers(2) = 1 2
End

Material 1					# Defining the material
  Name = "Material 1"
  Poisson ratio = .3
  Youngs modulus = 68.25E9
  Shell Thickness = 0.04
End

Boundary Condition 1				# Applying the boundary conditions
Target Boundaries(1) = 4
  Name = "XZ"
  U 2 = 0
  DNU 2 = 0
End

Boundary Condition 2
Target Boundaries(1) = 5
  Name = "Yz"
  U 1 = 0
  DNU 1 = 0
End

Boundary Condition 3
Target Nodes(1) = 5
  U 3 = 0
  U 2 = 0
  U 1 = 0
End

Boundary Condition 4
  Target Nodes(1) = 1
  Name = "Load X"
  U 1 Load  = Real 2000.0
End

Boundary Condition 5
  Target Nodes(1) = 7
  Name = "Load y"
  U 2 Load = Real -2000.0
End

```


The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/05-hemispherical-shell-point-load//Model_ElmerGUI)!
