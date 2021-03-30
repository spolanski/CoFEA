# Tested Finite Element codes
## CalculiX

The below section describes how the Cook's membrane model was created for Calculix solver. As mentioned in the results section, in order to define surface traction a separate app called PrePoMax has to be used. This application converts surface traction definition into the set of nodal loads.

```
** Material ++++++++++++++++++++++++++++++++++++++++++++++++

*Material, Name=Rubber      # Definition of material
  *Elastic,                 # Elastic properties
    70.0, 0.33              # Young's modulus and Poisson's ratio

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++

*SOLID SECTION, ELSET=Solid_part-1, Material=Rubber   # Assigning material and solid elements
                                                      # to the elements sets in mesh
** Steps +++++++++++++++++++++++++++++++++++++++++++++++++++

*STEP                                                 # Begin of analysis
    *STATIC                                           # Selection of elastic analysis

** Field outputs +++++++++++++++++++++++++++++++++++++++++++

*Node file                    # Extract nodal values
  RF, U
*El file                      # Extract element values
  S, E
*NODE PRINT, NSET=Vertex,     # Print displacement U2 to an external file
  U2

** Boundary conditions +++++++++++++++++++++++++++++++++++++
*Boundary           # Restrain movement in X, Y, Z
BC, 1, 1, 0
BC, 2, 2, 0
BC, 3, 3, 0

*Boundary           # Add symmetry condition
ZSYMM, 3, 3, 0

** Loading condition ++++++++++++++++++++
*Cload              # This is the nodal value converted from distributed force
176, 2, 31.25
194, 2, 62.5
191, 2, 62.5
175, 2, 31.25
193, 2, 62.5
190, 2, 62.5
192, 2, 62.5
189, 2, 62.5
180, 2, 31.25
179, 2, 31.25

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*End step                      # End on analysis

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA)!

## Code_Aster

This section describes how the model has been set up in Code_Aster solver
```
mesh = LIRE_MAILLAGE(identifier='0:1',                    # Read mesh
                     FORMAT='IDEAS',
                     UNITE=2)

model = AFFE_MODELE(identifier='1:1',                     # Define analysis type
                    AFFE=_F(MODELISATION=('3D', ),
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=mesh)

mater = DEFI_MATERIAU(identifier='2:1',                   # Define material model
                      ELAS=_F(E=70.0,
                              NU=0.3333))

materfl = AFFE_MATERIAU(identifier='3:1',                 # Assign material to the mesh
                        AFFE=_F(MATER=(mater, ),
                                TOUT='OUI'),
                        MODELE=model)

mecabc = AFFE_CHAR_MECA(identifier='4:1',                 # Define boundary conditions
                        DDL_IMPO=(_F(DX=0.0,
                                     DY=0.0,
                                     DZ=0.0,
                                     GROUP_MA=('BC', )),
                                  _F(DZ=0.0,
                                     GROUP_NO=('ZSYMM', ))),
                        MODELE=model)

mecach = AFFE_CHAR_MECA(identifier='5:1',                 # Define distributed load in Y direction
                        FORCE_FACE=_F(FY=6.25,
                                      GROUP_MA=('Load', )),
                        MODELE=model)

result = MECA_STATIQUE(identifier='7:1',                  # Define analysis type
                       CHAM_MATER=materfl,
                       EXCIT=(_F(CHARGE=mecabc),
                              _F(CHARGE=mecach)),
                       MODELE=model)

unnamed0 = CALC_CHAMP(identifier='8:1',                   # Define analysis output
                      CONTRAINTE=('SIEF_ELGA', 'SIEF_ELNO'),
                      CRITERES=('SIEQ_ELGA', 'SIEQ_ELNO'),
                      FORCE=('REAC_NODA', ),
                      RESULTAT=result)

table = POST_RELEVE_T(identifier='9:1',                   # Export nodal values to the file
                      ACTION=_F(GROUP_NO=('Vertex', ),
                                INTITULE='DISP',
                                NOM_CHAM='DEPL',
                                OPERATION=('EXTRACTION', ),
                                RESULTANTE=('DY', ),
                                RESULTAT=result))

IMPR_RESU(identifier='10:1',
          RESU=(_F(RESULTAT=unnamed0),
                _F(RESULTAT=result)),
          UNITE=3)

IMPR_TABLE(identifier='11:1',
           TABLE=table,
           UNITE=4)

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/)!

## Elmer

The following section describes how to set up a model in Elmer software

```
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/VeryFine_Quad_Hex"      # Mesh defintion
  Include Path ""
  Results Directory "Results/VeryFine_Quad_Hex" # Results directory
End

Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Solver Input File = case.sif  # solver input file
  Post File = case.vtu   # results file
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

Body 1
  Target Bodies(1) = 1
  Name = "Body 1" 
  Equation = 1 # Assign Linear Elasticity equation 
  Material = 1 # Assign material model
End

Solver 1
  # Small displacement Linear Elasticity solver
  Equation = Linear elasticity
  Calculate Loads = True
  Calculate Stresses = True
  Variable = -dofs 3 Displacement
  Procedure = "StressSolve" "StressSolver"
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
  Linear System Direct Method = MUMPS
End

Solver 2 
  # Solver used to export displacement data into the .dat file
  Equation = SaveScalars
  Procedure = "SaveData" "SaveScalars"
  Filename = results.dat
  Save Points = 5
  Save Coordinates(1,3) = 48.0 60.0 0.0
End

Equation 1
  Name = "LinearElasticity"
  Calculate Stresses = True
  Active Solvers(1) = 1
End

Material 1
  # Material definition
  Name = "Rubber"
  Youngs modulus = 70.0
  Poisson ratio = 0.33
End

# Boundary conditions:
# - restrain at one end
# - z-symmetry condition at sides
Boundary Condition 1
  Target Boundaries(1) = 1 
  Name = "FIX"
  Displacement 2 = 0
  Displacement 3 = 0
  Displacement 1 = 0
End

Boundary Condition 2
  Target Boundaries(1) = 3 
  Name = "SYMM"
  Displacement 3 = 0
End

Boundary Condition 3
  Target Boundaries(1) = 2 
  Name = "Force"
  Force 2 = 6.25 # Force value distributed over area in Y direction
End

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/)


