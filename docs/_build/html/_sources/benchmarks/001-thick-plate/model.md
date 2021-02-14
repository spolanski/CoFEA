# Model definition
## Benchmark aim

The aim of this study is to compare the results from a static analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. A thick plate geometry will be used to measure the software performance. The model described in this report was created on a basis of the article found in this [link](http://wufengyun.com:888/v6.14/books/bmk/ch04s02anf10.html).

The aim of this benchmark is to examine the stress $\sigma_{yy}$ of the thick plate at the point D. The target solution at this point is expected to be equal to 5.38 MPa. Additionally, the benchmark allow to test how easy is to apply pressure load condition.

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate)!

```{jupyter-execute}
:hide-code:
  from ipygany import Scene, TetraMesh
  mesh = TetraMesh.from_vtk('benchmarks/001-thick-plate/elipse.vtu')
  scene = Scene([mesh])
  scene
```
```{Tip}
The benchmark geometry shown above is interactive
```

```{figure} .   /sketch.png
---
width: 600px
alt: Thick plate benchmark
name: Thick plate benchmark
---
Sketch of the thick plate under pressure benchmark
```

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property               | Value                | Unit       |
|------------------------|----------------------|------------|
| Density $\rho$         | $7800.0$             | kg/$m^{3}$ |
| Young's modulus, E     | $2.10 \cdot 10^{11}$ | Pa         |
| Poisson's ratio, $\nu$ | 0.3                  | -          |

## Boundary conditions

- $u_y=0$ on face DCD′C′.
- $u_x=0$ on face ABA′B′.
- $u_y=u_x=0$ on face BCB′C′.
- $u_z=0$ on line EE′ (E is the midpoint of edge CC′; E′ is the midpoint of edge BB′).