# Results

Number of simulations with different element types and mesh size have been performed for the thick plate model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to use open-source software and achieve correct solution.
2. CalculiX and Code_Aster gave very similar response in tetrahedral meshes, the Elmer outperforms other solvers in linear tetrahedral and hexahedral quadratic meshes.
3. Calculix performs significanlty worse than other solvers in linear hexahedral meshes.
4. For the thick plate model, the quadratic shape tetrahedral mesh gives a more accurate answer than the linear one. The very fine linear hexahedral mesh achieve more precise solution than coarse quadratic hexahedral mesh.

```{figure} ./ccx_eliptic_membrane.png
---
width: 600px
alt: Calculix eliptic membrane results
name: Calculix eliptic membrane results
---
Results obtained with Calculix software and quadratic hexahedral mesh
```

## Linear tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 33.79 MPa               | 54.84 MPa               |    
| Code_Aster            | 33.58 MPa               | 54.88 MPa               |
| Elmer                 | 39.37 MPa               | 65.19 MPa               |

## Quadratic tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 73.09 MPa               |  88.42 MPa              |    
| Code_Aster            | 73.13 MPa               |  88.33 MPa              |
| Elmer                 | 69.26 MPa               |  85.46 MPa              |

```{figure} ./tet-comparison_eliptic_membrane.png
---
width: 600px
alt: Tetrahedral eliptic plate mesh comparison
name: Tetrahedral eliptic plate mesh comparison
---
Graph representing results of the simulation with tetrahedral mesh
```

## Linear hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 69.62 MPa               |  85.55 MPa              |    
| Code_Aster            | 70.49 MPa               |  85.40 MPa              |
| Elmer                 | 75.33 MPa               |  86.91 MPa              |

## Quadratic hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 85.85 MPa               |  92.99 MPa              |    
| Code_Aster            | 87 MPa                  |  92.21 MPa              |
| Elmer                 | 89.65 MPa               |  93.78 MPa              |

```{figure} ./hex-comparison_eliptic_membrane.png
---
width: 600px
alt: Hexahedral eliptic plate mesh comparison
name: Hexahedral eliptic plate mesh comparison
---
Graph representing results of the simulation with hexahedral mesh
```
