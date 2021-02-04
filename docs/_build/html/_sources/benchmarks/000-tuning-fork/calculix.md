# CalculiX

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
