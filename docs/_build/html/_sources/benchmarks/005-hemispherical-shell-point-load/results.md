# Results

Number of simulations with different element types and mesh size have been performed for the hemisphere shell model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to perform a plane stress analysis with pressure loading condition using open-source software and achieve a correct solution. In the current study, all solvers allow to obtain a stress value close to the target of $\sigma_{yy}=92.7 MPa$.
2. It can be seen that Calculix and Code_Aster generally provided similar output, with CalculiX being a slightly more precise in finer meshes.
3. Except of quadratic triangular meshes and fine quadratic quadrilateral mesh, Elmer was converging faster than others FE codes.

```{figure} ./shell.png
---
width: 600px
alt: Hemispherical shell membrane results
name: Hemispherical shell membrane results
---
Results obtained with Code_Aster software and linear hexahedral mesh
```


## Linear quadrilateral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 69.62 MPa               |  85.55 MPa              |    
| Code_Aster            | 70.49 MPa               |  85.40 MPa              |
| Elmer                 | 75.33 MPa               |  86.91 MPa              |

## Quadratic quadrilateral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 85.85 MPa               |  92.99 MPa              |    
| Code_Aster            | 87 MPa                  |  92.21 MPa              |
| Elmer                 | 89.65 MPa               |  93.78 MPa              |

```{figure} ./shell_comparison.png
---
width: 600px
alt: Quadrilateral eliptic plate mesh comparison
name: Quadrilateral eliptic plate mesh comparison
---
Graph representing results of the simulation with quadrilateral mesh
```
