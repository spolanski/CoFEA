# CalculiX

CalculiX supports rigid body moves out of the box. Below there is an explanation of the input file of CalculiX.

```

** Mesh ++++++++++++++++++++++++++++++++++++++++++++++++

*INCLUDE, INPUT=Mesh/TET-0-5.inp  # Path to mesh for ccx solver

** Material ++++++++++++++++++++++++++++++++++++++++++++++++

*Material, Name=Material-1      # Defining a material
*Density
7.829E-09                       # Defining a density
*Elastic
207000, 0.33                    # Defining Young modulus and Poisson's ratio

** Sections ++++++++++++++++++++++++++++++++++++++++++++++++

*Solid section, Elset=Fork-El_Section, Material=Material-1   # Assigning material and solid elements to the Elements sets in mesh

** Steps +++++++++++++++++++++++++++++++++++++++++++++++++++

*Step                           #  Begin of analysis
*Frequency                      # Selection of frequency analysis
12                              # Defining the number of modes to calculate  

** Field outputs +++++++++++++++++++++++++++++++++++++++++++

*Node file                      # Commands responsible for saving results     
RF, U
*El file
S, E

** End step ++++++++++++++++++++++++++++++++++++++++++++++++

*End step                      # End on analysis

```
