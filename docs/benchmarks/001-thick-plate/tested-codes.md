# Tested Finite Element codes
## CalculiX

CalculiX supports elastic simulation. Below there is an explanation of the input file.

```
** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/cofea-coarse-quad-hex.inp  # Path to mesh for ccx solver

** Material ++++++++++++++++++++++++++++++++++++++++++++++++

*MATERIAL, NAME=Steel                                    # Defining a material
    *DENSITY
        7800                                             # Defining a density
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
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate/Model_CalculiX)!

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
DEBUT(
      LANG='EN',
      PAR_LOT='NON',
      INFO=1,
     );

from pprint import pprint as pp

# Define material
STEEL   =DEFI_MATERIAU(
                       ELAS=_F(
                               E = 2.1e11,
                               NU = 0.3,
                              ),
                      );

mesh_nums ={
    20 : ["cfa-coarse-lin-hex"],
    21 : ["cfa-coarse-lin-tet"],
    22 : ["cfa-coarse-quad-hex"],
    23 : ["cfa-coarse-quad-tet"],
    24 : ["cfa-fine-lin-hex"],
    25 : ["cfa-fine-lin-tet"],
    26 : ["cfa-fine-quad-hex"],
    27 : ["cfa-fine-quad-tet"]
    }
mesh_list = [None] * len(mesh_nums.keys())

# Iterate for all meshes defined in astk with UNITE consistence with mesh_nums dictionary.
for ind, mesh_num in enumerate(mesh_nums.keys()):

    # Load mesh file
    mesh_list[ind] = LIRE_MAILLAGE(
                                   UNITE=mesh_num,
                                   FORMAT='IDEAS'
                                  );  			

    # Create groups of nodes according to all groups of elements
    # Additionaly create group with one node for comparison the results
    mesh_list[ind] = DEFI_GROUP(
                                reuse = mesh_list[ind],
                                MAILLAGE = mesh_list[ind],
                                CREA_GROUP_NO=(
                                               _F(TOUT_GROUP_MA = 'OUI',),
                                               _F(
                                                  NOM = 'D',
                                                  OPTION = 'ENV_SPHERE',
                                                  POINT = (2.0, 0.0, 0.6),
                                                  RAYON = 0.02,
                                                  PRECISION = 0.02
                                                 ),
                                              ),		
                               );

    # Change orientation of solids "peel"
    mesh_list[ind] = MODI_MAILLAGE(
                                   reuse = mesh_list[ind],
                                   MAILLAGE = mesh_list[ind],
                                   ORIE_PEAU_3D = _F(GROUP_MA = 'E_2_DIST'),
                                  );

    # Define analysis type
    Model = AFFE_MODELE(
                        MAILLAGE = mesh_list[ind],
                        AFFE = _F(
                                  TOUT = 'OUI',
                                  PHENOMENE = 'MECANIQUE',
                                  MODELISATION = '3D',		
                                 ),
                       );


    # Assign material to mesh and model
    Mater = AFFE_MATERIAU(
                          MAILLAGE = mesh_list[ind],
                          AFFE = _F(
                                    TOUT = 'OUI',
                                    MATER = STEEL,
                                   ),
                         );

    # Get list with names of nodes groups (node-sets)
    no_groups_names = mesh_list[ind].getGroupsOfNodes()

    # Find '_DC' name (C_A do not accept comprehension lists)
    for uy in no_groups_names:
        if uy.endswith('_DC'):            
            Uy_group_name = uy
            print(f"Uy_group_name: {Uy_group_name}")

    # Find '_MID' name (C_A do not accept comprehension lists)
    for uz in no_groups_names:
        if uz.endswith('_MID'):            
            Uz_group_name = uz
            print(f"Uz_group_name: {Uz_group_name}")

    # Define boundaries
    Bound = AFFE_CHAR_MECA(
                           MODELE = Model,
                           DDL_IMPO = (
                                       _F(GROUP_NO = Uz_group_name, DZ = 0.0,),
                                       _F(GROUP_NO = 'N_2_AB', DX = 0.0,),
                                       _F(GROUP_NO = Uy_group_name, DY = 0.0,),					  
                                       _F(GROUP_NO = 'N_3_BC', DX = 0.0, DY = 0.0,),
                                      ),
                            PRES_REP = _F(GROUP_MA = 'E_2_DIST', PRES = 1.0e6),
                          );

    # Solve
    Results = MECA_STATIQUE(      
                            MODELE = Model,
                            CHAM_MATER = Mater,
                            EXCIT = _F(CHARGE = Bound,),
                           );

    # Calculate the field of stresses extrapolated from Gauss point to nodes in Cartesian CS
    Results	= CALC_CHAMP(
                         reuse = Results,
                         RESULTAT = Results,
                         TOUT = 'OUI',
                         CONTRAINTE = 'SIGM_NOEU',
                        );

    # Extract value of normal stress in Y direction extrapolated to node D
    ResD = POST_RELEVE_T(
                         ACTION=(
                                 _F(
                                    INTITULE = 'Stress SIYY in point D',
                                    OPERATION = 'EXTRACTION',
                                    RESULTAT = Results,
                                    NOM_CHAM = 'SIGM_NOEU',
                                    NOM_CMP = ('SIYY'),
                                    GROUP_NO = 'D',
                                   ),
                                ),
                        );

    # Extract table to python object and save the value to dictionary
    resi=ResD.EXTR_TABLE()
    mesh_nums[mesh_num].append("{:e}".format(resi.SIYY.values()[0]))

    # Additionaly prepare mesh output enriched with fields of displacement, stresses in gauss points, and  stresses extrapolated to nodes
    IMPR_RESU(
              FORMAT = 'MED',
              UNITE = 80,
              RESU = _F(
                        MAILLAGE = mesh_list[ind],
                        RESULTAT = Results,		  
                        NOM_CHAM = ('DEPL', 'SIEF_ELGA','SIGM_NOEU'),                   
                       ),
             );

# Pretty print the dictionary with stresses
print("Results:")
pp(mesh_nums)
FIN();

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate/Model_Code_Aster)!

## Elmer

Elmer supports elastic simulations out of the box. Below there is an explanation of solver input file.

```
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/cfa-fine-lin-hex"               # Path to the mesh
  Include Path ""
  Results Directory "Results/cfa-fine-lin-hex"      # Path to results directory
End

Simulation                                          # Settings and constants for simulation
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

Body 1                                              # Assigning the material and equations to the mesh
  Target Bodies(1) = 1
  Name = "Body Property 1"
  Equation = 1
  Material = 1
End

Solver 1                                            # Solver settings
  Equation = Linear elasticity
  Calculate Loads = True
  Calculate Stresses = True
  Procedure = "StressSolve" "StressSolver"
  Variable = -dofs 3 Displacement
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
  Linear System Solver = Iterative
  Linear System Iterative Method = BiCGStab
  Linear System Max Iterations = 500
  Linear System Convergence Tolerance = 1.0e-10
  BiCGstabl polynomial degree = 2
  Linear System Preconditioning = ILU0
  Linear System ILUT Tolerance = 1.0e-3
  Linear System Abort Not Converged = False
  Linear System Residual Output = 10
  Linear System Precondition Recompute = 1
End

Equation 1                                          # Setting the active solvers
  Name = "Equation 1"
  Plane Stress = True
  Plane Stress = True
  Calculate Stresses = True
  Active Solvers(1) = 1
End

Material 1                                          # Defining the material
  Name = "Steel (carbon - generic)"
  Heat Capacity = 1265.0
  Poisson ratio = 0.3
  Electric Conductivity = 1.449e6
  Electric Conductivity = 1.449e6
  Porosity Model = Always saturated
  Youngs modulus = 2.1e11
  Density = 7800.0
  Mesh Poisson ratio = 0.3
  Youngs modulus = 2.1e11
  Heat expansion Coefficient = 13.8e-6
  Heat Conductivity = 44.8
  Poisson ratio = 0.3
  Electric Conductivity = 1.449e6
  Youngs modulus = 2.1e11
  Sound speed = 5100.0
  Electric Conductivity = 1.449e6
  Electric Conductivity = 1.449e6
  Poisson ratio = 0.3
End

Boundary Condition 1                                # Applying the boundary conditions
  Target Boundaries(1) = 3
  Name = "AB"
  Displacement 1 = 0
End

Boundary Condition 2
  Target Boundaries(1) = 6
  Name = "CD"
  Displacement 2 = 0
End

Boundary Condition 3
  Target Boundaries(1) = 4
  Name = "BC"
  Displacement 2 = 0
  Displacement 1 = 0
End

Boundary Condition 4
  Target Boundaries(1) = 1
  Name = "LOAD"
  Normal Force = 1e6
End

Boundary Condition 5
  Target Boundaries(1) = 9
  Name = "EE"
  Displacement 3 = 0
End

```


The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate/Model_ElmerGUI)!
