<!---
# Model setup

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
-->
# Model definition

The aim of this study is to compare the results from a static analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. A thick plate geometry will be used to measure the software performance. The model described in this report was created on a basis of the article found in this [link](http://wufengyun.com:888/v6.14/books/bmk/ch04s02anf10.html).

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate)!


## Expected solution

This is a test recommended by the National Agency for Finite Element Methods and Standards (U.K.): Test LE10 from NAFEMS Publication TNSB, Rev. 3, “The Standard NAFEMS Benchmarks,” October 1990.

Target solution: Direct stress,  5.38 MPa at point D.

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property              | Value                | Unit       |
|-----------------------|----------------------|------------|
| Density $\rho$        | $7800.0$             | kg/$m^{3}$ |
| Young's modulus, E    | $2.10 \cdot 10^{11}$ | Pa         |
| Poissons ratio, $\nu$ | 0.3                  | -          |

## Boundary conditions

- $u_y=0$ on face DCD′C′.
- $u_x=0$ on face ABA′B′.
- $u_y=u_x=0$ on face BCB′C′.
- $u_z=0$ on line EE′ (E is the midpoint of edge CC′; E′ is the midpoint of edge BB′).



## Benchmark aim

The aim of this benchmark is to examine the stress $\alpha_{yy}$ of the thick plate in point D.
