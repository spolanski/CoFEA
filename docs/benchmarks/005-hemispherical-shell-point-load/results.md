# Results

Number of simulations with different element types and mesh size have been performed for the hemisphere shell model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to perform a plane stress analysis with pressure loading condition using open-source software and achieve a correct solution. In the current study, all solvers allow to obtain a stress value close to the target of $\sigma_{yy}=92.7 m$.
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
| CalculiX              | 0.000306 m              |  0.0000325 m            |    
| Code_Aster            | 0.163 m                 |  0.192 m                |
| Elmer                 | 0.009578 m              |  0.033597 m             |

## Quadratic quadrilateral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 0.0000431 m             |  0.0000792 m            |    
| Code_Aster            | 0.147 m                 |  0.184 m                |
| Elmer                 | no data                 | no data                 |

```{figure} ./shell_comrison.png
---
width: 600px
alt: Quadrilateral eliptic plate mesh comrison
name: Quadrilateral eliptic plate mesh comrison
---
Graph representing results of the simulation with quadrilateral mesh
```
