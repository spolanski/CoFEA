# Results

Number of simulations with different element types and mesh size have been performed for the hemisphere shell model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is hard to perform a shell analysis with force loading condition using open-source software and achieve a correct solution. In the current study, only code_aster benchmark mesh was able to obtain a displacement value close to the target of $u_{x}=0.185 m$.
2. To obtain precise results with Elmer it is needed to use finer meshes and calculate normal vectors before starting the calculations (mesh.director). For now (27.03.2021) Elmer doesn't support quadratic shell elements. Please remember that shell solver is under development.
3. Calculix was unable to produce correct results with shell and solid elements. For more detailed information please read chapter below.
4. Code_Aster support QUAD_9 instead QUAD_8 elements. Fortunately the solver itself contains a mesh converter to this type of elements.


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

## Numerous models in Calculix
In order to obtain correct results with Calculix 3 models were prepared:
- hemisphere model with use of shell S8 elements as described in NAFEMS benchmark,
- hemisphere model with use of solid C3D20R elements as described in NAFEMS benchmark,
- full hemisphere model with use of shell S8 elements modeled without symmetry boundary conditions,

Neither of these models produced correct results. With shell models is possible to obtain correct displacement contour but incorrect value of seeking variable. On the contrary with solid model is possible to obtain correct results in terms of specific displacement in point A, but not in contour plot. Please see the image below as proof of statement.


```{figure} ./ccx_comparison.png
---
width: 700px
alt: CalculiX results comparison
name: CalculiX results comparison
---
Graph representing results of different models results in CalculiX from left: S8 shell elements, solid C3D20R elements, S8 shell full hemisphere,
