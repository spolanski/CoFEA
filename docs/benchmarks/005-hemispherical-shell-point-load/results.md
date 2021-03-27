# Results

Number of simulations with different element types and mesh size have been performed for the hemisphere shell model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is hard to perform a shell analysis with force loading condition using open-source software and achieve a correct solution. In the current study, only code_aster benchmark mesh was able to obtain a displacement value close to the target of $u_{x}=0.185 m$.
2. To obtain precise results with Elmer it is needed to use finer meshes and calculate normal vectors before starting the calculations.
3. Calculix was unable to produce correct results with shell elements.

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

```{figure} ./shell_comparison.png
---
width: 600px
alt: Quadrilateral shell mesh comparison
name: Quadrilateral shell mesh comparison
---
Graph representing results of the simulation with quadrilateral mesh
```
