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

## Linear tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $564.55 Hz$             | $490.92 Hz$             | $455.64 Hz$               |    
| Code_Aster            | $564.48 Hz$             | $490.90 Hz$             | $455.63 Hz$               |
| Elmer                 | $564.48 Hz$             | $490.90 Hz$             | $455.63 Hz $              |


```{figure} ./Linear-tetrahedral-mesh.png
---
width: 500px
alt: Linear tetrahedral mesh Results
name: Liner tetrahedral mesh Fork Results
---
Chart representing results of the simulation with linear tetrahedral mesh
```
### Error obtained with linear tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $28.30 \%$              | $11.57 \%$              | $3.55 \%$                 |    
| Code_Aster            | $28.29 \%$              | $11.57 \%$              | $3.55 \%$                 |
| Elmer                 | $28.29 \%$              | $11.57 \%$              | $3.55 \%$                 |


## Linear hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $388.67 Hz$             | $415.79 Hz$             | $434.17 Hz$               |    
| Code_Aster            | $496.87 Hz$             | $455.34 Hz$             | $444.22 Hz$               |
| Elmer                 | $496.87 Hz$             | $455.34 Hz$             | $444.22 Hz$               |

```{figure} ./Linear-hexahedral-mesh.png
---
width: 500px
alt: Linear hexahedral mesh Results
name: Linear hexahedral mesh Fork Results
---
Chart representing results of the simulation with linear hexahedral mesh
```
### Error obtained with linear hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $11.66 \%$              | $5.50 \%$               | $1.32 \%$                 |    
| Code_Aster            | $12.93 \%$              | $3.49 \%$               | $0.96 \%$                 |
| Elmer                 | $12.93 \%$              | $3.49 \%$               | $0.96 \%$                 |

## Quadratic tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $441.14 Hz$             | $440.29 Hz$             | $440.0088 Hz$             |    
| Code_Aster            | $441.16 Hz$             | $440.29 Hz$             | $440.0092 Hz$             |
| Elmer                 | $441.26 Hz$             | $440.30 Hz$             | $440.0094 Hz$             |

```{figure} ./Quadratic-tetrahedral-mesh.png
---
width: 500px
alt: Quadratic tetrahedral mesh Results
name: Quadratic tetrahedral mesh Fork Results
---
Chart representing results of the simulation with quadratic tetrahedral mesh
```
### Error obtained with quadratic tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.26 \%$               | $0.0662 \%$             | $0.002 \%$                |    
| Code_Aster            | $0.27 \%$               | $0.0672 \%$             | $0.002 \%$                |
| Elmer                 | $0.29 \%$               | $0.0685 \%$             | $0.002 \%$                |


## Quadratic hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $440.57 Hz$             | $440.34 Hz$             | $440.0529 Hz$             |    
| Code_Aster            | $441.10 Hz$             | $440.49 Hz$             | $440.0907 Hz$             |
| Elmer                 | $441.10 Hz$             | $440.49 Hz$             | $440.0907 Hz$             |

```{figure} ./Quadratic-hexahedral-mesh.png
---
width: 500px
alt: Quadratic hexahedral mesh Results
name: Quadratic hexahedral mesh Fork Results
---
Chart representing results of the simulation with quadratic hexahedral mesh
```
### Error obtained with quadratic hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.13 \%$               | $0.0776 \%$             | $0.012 \%$                |    
| Code_Aster            | $0.25 \%$               | $0.1114 \%$             | $0.021 \%$                |
| Elmer                 | $0.25 \%$               | $0.1114 \%$             | $0.021 \%$                |


## Quadratic wedge mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $441.16 Hz$             | $440.32 Hz$             | $440.0090 Hz$             |    
| Code_Aster            | $441.35 Hz$             | $440.34 Hz$             | $440.0104 Hz$             |
| Elmer                 | $441.35 Hz$             | $440.34 Hz$             | $440.0104 Hz$             |

```{figure} ./Quadratic-wedge-mesh.png
---
width: 500px
alt: Quadratic wedge mesh Results
name: Quadratic wedge mesh Fork Results
---
Chart representing results of the simulation with quadratic wedge mesh
```
### Error obtained with quadratic wedge mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.26 \%$               | $0.0735 \%$             | $0.0020(45) \%$           |    
| Code_Aster            | $0.31 \%$               | $0.0783 \%$             | $0.0002(36) \%$           |
| Elmer                 | $0.31 \%$               | $0.0783 \%$             | $0.0002(36) \%$           |

## Codes comparison

| Eigenfrequency | Commercial code | Calculix | Code Aster |  Elmer  |
|----------------|:---------------:|:--------:|:----------:|:-------:|
|              1 |      440.33     |  440.05  |   440.91   |  440.91 |
|              2 |      675.80     |  673.51  |   673.57   |  673.57 |
|              3 |     1689.51     |  1689.30 |   1689.37  | 1689.37 |
|              4 |     1827.55     |  1825.55 |   1825.63  | 1825.63 |
|              5 |     2788.66     |  2777.73 |   2777.56  | 2777.56 |


## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to use open-source software and achieve correct solution.
2. Although all three solvers gave very similar response, it feels like Calculix and Elmer were the most straightforward to set up. They picked up rigid body modes without any additional settings. On the other hand, Code_Aster had to be set up so that it searches only for non-rigid body modes (this is possible with setting called 'Bande') or the model has to be constrained.
3. Despite the mentioned difference in the solver setup, Code_Aster and Elmer seem to give almost the same answers.
4. For the tuning fork model, the quadratic shape function give a lot more accurate answer than the linear one. The very fine linear hexahedral mesh achieve the same order of accuracy as the coarse quadratic tetrahedral mesh.
