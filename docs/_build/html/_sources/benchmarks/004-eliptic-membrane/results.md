# Results

Number of simulations with different element types and mesh size have been performed for the eliptic membrane model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to perform a plane stress analysis with pressure loading condition using open-source software and achieve a correct solution. In the current study, all solvers allow to obtain a stress value close to the target of $\sigma_{yy}=92.7 MPa$.
2. It can be seen that Calculix and Code_Aster generally provided similar output, with CalculiX being a slightly more precise in finer meshes.
3. Except of quadratic triangular meshes and fine quadratic quadrilateral mesh, Elmer was converging faster than others FE codes.

```{figure} ./ccx_eliptic_membrane.png
---
width: 600px
alt: Calculix eliptic membrane results
name: Calculix eliptic membrane results
---
Results obtained with Calculix software and quadratic hexahedral mesh
```

## Linear triangular mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 33.79 MPa               | 54.84 MPa               |    
| Code_Aster            | 33.58 MPa               | 54.88 MPa               |
| Elmer                 | 39.37 MPa               | 65.19 MPa               |

## Quadratic triangular mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 73.09 MPa               |  88.42 MPa              |    
| Code_Aster            | 73.13 MPa               |  88.33 MPa              |
| Elmer                 | 69.26 MPa               |  85.46 MPa              |

```{figure} ./tri-comparison_eliptic_membrane.png
---
width: 600px
alt: Triangular eliptic plate mesh comparison
name: Triangular eliptic plate mesh comparison
---
Graph representing results of the simulation with triangular mesh
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

```{figure} ./quad-comparison_eliptic_membrane.png
---
width: 600px
alt: Quadrilateral eliptic plate mesh comparison
name: Quadrilateral eliptic plate mesh comparison
---
Graph representing results of the simulation with quadrilateral mesh
```
