# Tuning fork benchmark

<script src="https://code.jquery.com/jquery-2.1.4.js"></script>
   <script>
      function showIframeMapOnClick() {
         $("#myDiv").html("<iframe id='iFrameMap' src='https://blogtechniczny.pl/paraview-glance/index.html?name=fork.vtk&url=https://blogtechniczny.pl/para-files/fork.vtk' width='100%' height='550px' style=''></iframe>");
      }
   </script>

<div id="myDiv">
   <input width="100%" type="image" ID="Image1" onclick="showIframeMapOnClick();return false" src="../../_static/fork.png"  />
</div>

```{tip}
Click on the image above to play with 3D object in ParaView Glance!
```

## Model definition

The aim of this study is to compare the results from a modal analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. A tuning fork geometry will be used to measure the software performance. The model described in this report was created on a basis of the article found in this [link](http://pubs.sciepub.com/ajme/4/7/16/index.html).

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/Benchmarks/00-Tuning-Fork)!

```{figure} ./fork-geo-results.png
---
width: 400px
alt: Fork original Results
name: Fork Results
---
Tuning fork geometry and its' vibration modes
```


## Approximated solution

It is possible to estimate the frequency of the fork using the fixed-free cantilever beam equation.

$$
   \begin{eqnarray}
      f_{1} = \frac{1.875^{2}}{2 \pi L^{2}} \sqrt{\frac{E I}{\rho A}} = 495.11 [Hz]
   \end{eqnarray}
$$

- Length of the prong, $L=0.0709$ [m]
- Young's modulus, $E=207$ [GPa]
- Material density, $\rho = 7829 $ [kg/$m^{3}$]
- Moment of inertia $I = \frac{a^{4}}{12}$ [$m^{4}$]
- Cross-sectional area of the prong, $A = a^{2}$

Based on the expected value of frequency $f=440$ Hz, the relative error can be measured as follows:

$$
   \begin{eqnarray}
      Error = \left\lvert \frac{495.11 - 440.0}{440} \cdot 100 \% \right\rvert = 12.5 \%
   \end{eqnarray}
$$

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property              | Value                | Unit       |
|-----------------------|----------------------|------------|
| Density $\rho$        | $7829.0$             | kg/$m^{3}$ |
| Young's modulus, E    | $2.07 \cdot 10^{11}$ | Pa         |
| Poissons ratio, $\nu$ | 0.33                 | -          |

## Boundary conditions

It is a free body modal simulation therefore there is no boundary conditions assigned to the tuning fork.

## Results

Number of simulations with different element types and mesh size have been performed for the tuning model. The animation below shows the results from the Calculix code.

```{figure} ./movie.gif
---
width: 600px
alt: Fork gif
name: Fork gif
---
Tuning fork geometry and its' 1st vibration mode
```

### Linear tetrahedral mesh

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
#### Error obtained with linear tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $28.30 \%$              | $11.57 \%$              | $3.55 \%$                 |    
| Code_Aster            | $28.29 \%$              | $11.57 \%$              | $3.55 \%$                 |
| Elmer                 | $28.29 \%$              | $11.57 \%$              | $3.55 \%$                 |


### Linear hexahedral mesh

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
#### Error obtained with linear hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $11.66 \%$              | $5.50 \%$               | $1.32 \%$                 |    
| Code_Aster            | $12.93 \%$              | $3.49 \%$               | $0.96 \%$                 |
| Elmer                 | $12.93 \%$              | $3.49 \%$               | $0.96 \%$                 |

### Quadratic tetrahedral mesh

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
#### Error obtained with quadratic tetrahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.26 \%$               | $0.0662 \%$             | $0.002 \%$                |    
| Code_Aster            | $0.27 \%$               | $0.0672 \%$             | $0.002 \%$                |
| Elmer                 | $0.29 \%$               | $0.0685 \%$             | $0.002 \%$                |


### Quadratic hexahedral mesh

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
#### Error obtained with quadratic hexahedral mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.13 \%$               | $0.0776 \%$             | $0.012 \%$                |    
| Code_Aster            | $0.25 \%$               | $0.1114 \%$             | $0.021 \%$                |
| Elmer                 | $0.25 \%$               | $0.1114 \%$             | $0.021 \%$                |


### Quadratic wedge mesh

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
> Error obtained with quadratic wedge mesh

| Solver                |Mesh element size = 2mm  | Mesh element size = 1mm | Mesh element size = 0.5mm |
|-----------------------|-----------------------  |-------------------------|---------------------------|
| CalculiX              | $0.26 \%$               | $0.0735 \%$             | $0.0020(45) \%$           |    
| Code_Aster            | $0.31 \%$               | $0.0783 \%$             | $0.0002(36) \%$           |
| Elmer                 | $0.31 \%$               | $0.0783 \%$             | $0.0002(36) \%$           |

### Codes comparison

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
