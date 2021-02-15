# Results

Number of simulations with different element types and mesh size have been performed for the thick plate model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to use open-source software and achieve correct solution.
2. CalculiX and Code_Aster gave very similar response in tetrahedral meshes, the Elmer shines in hexahedral quadratic meshes.
3. Calculix performs significanlty worse than other solvers in linear hexahedral meshes. 
4. For the thick plate model, the quadratic shape tetrahedral mesh gives a more accurate answer than the linear one. The very fine linear hexahedral mesh achieve more precise solution than coarse quadratic hexahedral mesh.


## Linear tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -1.51 MPa               | -4.38 MPa               |    
| Code_Aster            | -1.51 MPa               | -4.38 MPa               |
| Elmer                 | -2.84 MPa               | -2.53 MPa               |

## Quadratic tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -5.45 MPa               |  -5.77 MPa              |    
| Code_Aster            | -5.51 MPa               |  -5.85 MPa              |
| Elmer                 | -2.78 MPa               |  -3.51 MPa              |

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
| Elmer                 | -1.02 MPa               |  -5.02 MPa              |

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
