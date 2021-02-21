# Results

Number of simulations with different element types and mesh size have been performed for the thick plate under pressure model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to perform a structural analysis with pressure loading condition using open-source software and achieve a correct solution. In the current study, fairly coarse meshes have been tested and they allow to obtain a stress value close to the target of $\sigma_{yy}=5.38 MPa$. An additional test with a very fine mesh has been run and all tested FE codes converged to the target value.
2. It can be seen that Calculix and Code_Aster generally provided similar output apart for the case of linear hex mesh. It may indicate that a slightly different element formulation for linear hexahedral meshes was used.
3. The results from Elmer show a different convergence behaviour comparing to other FE codes. While this behaviour can be a result of different numerical scheme implementation, it should also be highlighted that FE meshes used in Elmer runs were slightly different compared to the runs in other codes. This difference was caused by the fact that the meshes used in Calculix and Code_Aster came as an output from meshpresso converter and those seem not to be compatible with Elmer. It looks like the 3D geometry requires all type of elements to be provided (3D hex/tet, 2D tri/quad and 1D wires) while at the current stage, the meshpresso provides only 3D or 2D elements. However, it was also noted that ElmerGUI struggles to import some type of .UNV meshes created in the Salome environment. Especially, the quadratic hexahedral mesh type seems to be problematic.

```{figure} ./ccx_output.png
---
width: 600px
alt: Calculix results
name: Calculix results
---
Results obtained with Calculix software and quadratic hexahedral mesh
```

## Linear tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -1.51 MPa               | -4.38 MPa               |    
| Code_Aster            | -1.51 MPa               | -4.38 MPa               |
| Elmer                 | -2.64 MPa               | -5.49 MPa               |

## Quadratic tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -5.45 MPa               |  -5.77 MPa              |    
| Code_Aster            | -5.51 MPa               |  -5.85 MPa              |
| Elmer                 | -4.58 MPa               |  -5.50 MPa              |

```{figure} ./tet-comparison_thick_plate.png
---
width: 600px
alt: Tetrahedral mesh comparison
name: Tetrahedral mesh comparison
---
Graph representing results of the simulation with tetrahedral mesh
```

## Linear hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -2.75 MPa               |  -3.08 MPa              |    
| Code_Aster            | -4.05 MPa               |  -5.42 MPa              |
| Elmer                 | -4.52 MPa               |  -5.02 MPa              |

## Quadratic hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -7.34 MPa               |  -5.65 MPa              |    
| Code_Aster            | -7.39 MPa               |  -5.66 MPa              |
| Elmer                 | -5.56 MPa               |  -5.65 MPa              |

```{figure} ./hex-comparison_thick_plate.png
---
width: 600px
alt: Hexahedral mesh comparison
name: Hexahedral mesh comparison
---
Graph representing results of the simulation with hexahedral mesh
```
