# Tested Finite Element codes
## CalculiX

CalculiX supports elastic simulation. Below there is an explanation of the input file.

```
** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/fine-lin-hex.inp		# Path to mesh for ccx solver

** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*MATERIAL, NAME=Steel				# Defining a material
*DENSITY
 7800						# Defining a density
*ELASTIC,
2.1e11, 0.3					# Defining Young modulus and Poisson's ratio

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++

*SOLID SECTION, ELSET=ELIPSE, MATERIAL=Steel 	# Assigning material and plane stress elements
0.1,						# to the elements sets in mesh and adding thickness

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
AB,1,1,0
*BOUNDARY
CD,2,2,0

** Boundary conditions(adding pressure) ++++++++++++++++++++

*DLOAD
*INCLUDE, INPUT=Pressure/fine-lin-hex.dlo

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*END STEP					# End on analysis


```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/04-eliptic-membrane/model_setup/Model_CalculiX)!

### How to apply pressure boundary condition

Please open your mesh with CalculiX GraphiX in read mode using:

```
cgx -c mesh_file.inp
```
Then in CGX window please click right button of mouse and choose Toggle command line. In command line please write:

```
comp NODESET do
send NODESET abq press value_of_press
```
In the same directory should appear file called NODESET.dlo which need to be included in *DLOAD section to apply pressure to boundary.
Positive value of pressure goes is compressing the element face.

## Code_Aster

Code_Aster supports elastic simulation. Below there is an explanation of the input file.


```
mesh = LIRE_MAILLAGE(identifier='0:1',				# Reading a mesh
                     FORMAT='IDEAS',
                     UNITE=80)

model = AFFE_MODELE(identifier='1:1',				# Assignig plane stress
                    AFFE=_F(MODELISATION=('C_PLAN', ),		# elements to mesh
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=mesh)

mater = DEFI_MATERIAU(identifier='2:1',				# Defining elastic material
                      ELAS=_F(E=210000000000.0,
                              NU=0.3))

materfl = AFFE_MATERIAU(identifier='3:1',			# Assigning material to model
                        AFFE=_F(MATER=(mater, ),
                                TOUT='OUI'),
                        MODELE=model)

mecabc = AFFE_CHAR_MECA(identifier='4:1',			# Applying boundary conditions
                        DDL_IMPO=(_F(DX=0.0,			# displacement = 0
                                     GROUP_MA=('AB', )),	# to the selected group of elements
                                  _F(DY=0.0,
                                     GROUP_MA=('CD', ))),
                        MODELE=model)

mecach = AFFE_CHAR_MECA(identifier='5:1',			# Applying pressure to the
                        MODELE=model,				# group of elements
                        PRES_REP=_F(GROUP_MA=('BC', ),
                                    PRES=-10000000.0))

result = MECA_STATIQUE(identifier='6:1',			# Defining the results of
                       CHAM_MATER=materfl,			# simulation
                       EXCIT=(_F(CHARGE=mecabc),
                              _F(CHARGE=mecach)),
                       MODELE=model)

SYY = CALC_CHAMP(identifier='7:1',				# Calculating stresses in
                 CHAM_MATER=materfl,				# computed domain
                 CONTRAINTE=('SIGM_NOEU', ),
                 MODELE=model,
                 RESULTAT=result)

IMPR_RESU(identifier='8:1',					# Saving the results
          FORMAT='MED',	  
          RESU=(_F(RESULTAT=result),
                _F(RESULTAT=SYY)),
          UNITE=80)

FIN()

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/04-eliptic-membrane/model_setup//Model_Code_Aster)!

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
  Target Bodies(1) = 10
  Name = "Body Property 1"
  Equation = 1
  Material = 1
End

Solver 2					# Solver settings
  Equation = Linear elasticity
  Procedure = "StressSolve" "StressSolver"
  Calculate Stresses = True
  Variable = -dofs 2 Displacement
  Exec Solver = Always
  Stabilize = True
  Bubbles = False
  Lumped Mass Matrix = False
  Optimize Bandwidth = True
  Steady State Convergence Tolerance = 1.0e-5
  Nonlinear System Convergence Tolerance = 1.0e-7
  Nonlinear System Max Iterations = 20
  Nonlinear System Newton After Iterations = 3
  Nonlinear System Newton After Tolerance = 1.0e-3
  Nonlinear System Relaxation Factor = 1
  Linear System Solver = Direct
  Linear System Direct Method = Umfpack
End

Solver 1					# Saving the results from node at point D
  Equation = SaveScalars
  Save Points = 26
  Procedure = "SaveData" "SaveScalars"
  Filename = file.dat
  Exec Solver = After Simulation
End

Equation 1					# Setting active solvers
  Name = "STRESS"
  Calculate Stresses = True
  Plane Stress = True				# Turning on plane stress simulation
  Active Solvers(1) = 2
End

Equation 2
  Name = "DATA"
  Active Solvers(1) = 1
End

Material 1					# Defining the material
  Name = "STEEL"
  Poisson ratio = 0.3
  Porosity Model = Always saturated
  Youngs modulus = 2.1e11
End

Boundary Condition 1				# Applying the boundary conditions
  Target Boundaries(1) = 12
  Name = "AB"
  Displacement 1 = 0
End

Boundary Condition 2
  Target Boundaries(1) = 13
  Name = "CD"
  Displacement 2 = 0
End

Boundary Condition 3
  Target Boundaries(1) = 14
  Name = "BC"
  Normal Force = 10e6
End

```


The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/04-eliptic-membrane/model_setup//Model_ElmerGUI)!
