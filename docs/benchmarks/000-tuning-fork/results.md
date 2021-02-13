# Results

Number of simulations with different element types and mesh size have been performed for the tuning model. The animation below shows the results from the Calculix code.

```{figure} ./movie.gif
---
width: 600px
alt: Fork gif
name: Fork gif
---
Tuning fork geometry and its' 1st vibration mode
```

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to use open-source software and achieve correct solution.
2. Although all three solvers gave very similar response, it feels like Calculix and Elmer were the most straightforward to set up. They picked up rigid body modes without any additional settings. On the other hand, Code_Aster had to be set up so that it searches only for non-rigid body modes (this is possible with setting called 'Bande') or the model has to be constrained.
3. Despite the mentioned difference in the solver setup, Code_Aster and Elmer seem to give almost the same answers.
4. For the tuning fork model, the quadratic shape function give a lot more accurate answer than the linear one. The very fine linear hexahedral mesh achieve the same order of accuracy as the coarse quadratic tetrahedral mesh.

## Codes comparison

| Eigenfrequency | Commercial code    | Calculix    | Code Aster    |  Elmer     |
|----------------|:------------------:|:-----------:|:-------------:|:----------:|
|              1 |      440.33 Hz     |  440.05 Hz  |   440.91 Hz   |  440.91 Hz |
|              2 |      675.80 Hz     |  673.51 Hz  |   673.57 Hz   |  673.57 Hz |
|              3 |     1689.51 Hz     |  1689.30 Hz |   1689.37 Hz  | 1689.37 Hz |
|              4 |     1827.55 Hz     |  1825.55 Hz |   1825.63 Hz  | 1825.63 Hz |
|              5 |     2788.66 Hz     |  2777.73 Hz |   2777.56 Hz  | 2777.56 Hz |

```{figure} ./code-comparison.png
---
width: 600px
alt: FE codes comparison
name: FE codes comparison
---
Comparison of FE codes
```


## Linear tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              |  564.55 Hz              |  490.92 Hz              |  455.64 Hz                |    
| Code_Aster            |  564.48 Hz              |  490.90 Hz              |  455.63 Hz                |
| Elmer                 |  564.48 Hz              |  490.90 Hz              |  455.63 Hz                |

## Quadratic tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              |  441.14 Hz              |  440.29 Hz              |  440.00 Hz              |    
| Code_Aster            |  441.16 Hz              |  440.29 Hz              |  440.00 Hz              |
| Elmer                 |  441.26 Hz              |  440.30 Hz              |  440.00 Hz              |

```{figure} ./tet-comparison.png
---
width: 600px
alt: Tetrahedral mesh comparison
name: Tetrahedral mesh comparison
---
Graph representing results of the simulation with tetrahedral mesh 
```

## Linear hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              |  388.67 Hz              |  415.79 Hz              |  434.17 Hz                |    
| Code_Aster            |  496.87 Hz              |  455.34 Hz              |  444.22 Hz                |
| Elmer                 |  496.87 Hz              |  455.34 Hz              |  444.22 Hz                |

## Quadratic hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              |  440.57 Hz              |  440.34 Hz              |  440.05 Hz              |    
| Code_Aster            |  441.10 Hz              |  440.49 Hz              |  440.09 Hz              |
| Elmer                 |  441.10 Hz              |  440.49 Hz              |  440.09 Hz              |

```{figure} ./hex-comparison.png
---
width: 600px
alt: Hexahedral mesh comparison
name: Hexahedral mesh comparison
---
Graph representing results of the simulation with hexahedral mesh 
```
