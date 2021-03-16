# Model definition
## Benchmark aim

The aim of this study is to compare the results from a modal analysis performed in different Finite-Element codes. A tuning fork geometry will be used to measure the software performance. For the tuning fork geometry used in this study, the first frequency of vibration is expected to be close to 440 Hz ([original study](http://pubs.sciepub.com/ajme/4/7/16/index.html)).

This benchmark checks as well if it is possible to run a free-free modal analysis and how easy it can be performed.

Simulation input files used in this study can be found on [CoFEA GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/00-Tuning-Fork).

```{jupyter-execute}
:hide-code:
from ipygany import Scene, TetraMesh
mesh = TetraMesh.from_vtk('docs/benchmarks/000-tuning-fork/fork.vtk')
scene = Scene([mesh])
scene
```
```{Tip}
The tuning fork geometry shown above is interactive
```

```{figure} ./fork-geo-results.png
---
width: 400px
alt: Fork original Results
name: Fork Results
---
Tuning fork geometry and its' vibration modes
```

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property              | Value                | Unit       |
|-----------------------|----------------------|------------|
| Density $\rho$        | $7829.0$             | kg/$m^{3}$ |
| Young's modulus, E    | $2.07 \cdot 10^{11}$ | Pa         |
| Poissons ratio, $\nu$ | 0.33                 | -          |

## Boundary conditions

It is a free body modal simulation therefore there is no boundary conditions assigned to the tuning fork.
