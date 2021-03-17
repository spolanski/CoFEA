# Model definition
## Benchmark aim

The aim of this study is to compare the results from a static analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. A thick plate geometry will be used to measure the software performance. The model described in this report was created on a basis of the article found in this [link](https://abaqus-docs.mit.edu/2017/English/SIMACAEBMKRefMap/simabmk-c-le3.htm).

The aim of this benchmark is to examine the $u_x$ of the shell at the point A. The target solution at this point is expected to be equal to 0.185 m.

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/05-hemispherical-shell-point-load)!

```{jupyter-execute}
  :hide-code:
  import numpy as np
  import pyvista as pv
  from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink, Layout, VBox, HBox
  from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps



  mesh = TetraMesh.from_vtk('benchmarks/005-hemispherical-shell-point-load/hemisperical-shell-points-load.vtu', show_edges = True)

  u_min = 4.4e-6
  u_max = 1.8e-1

  # Colorize by height
  colored_mesh = IsoColor(mesh, input=('u','X1'), min=u_min, max=u_max)

  # Create a slider that will dynamically change the boundaries of the colormap
  colormap_slider_range = FloatRangeSlider(value=[u_min, u_max], min=u_min, max=u_max, step=(u_max - u_min) / 100.)

  jslink((colored_mesh, 'range'), (colormap_slider_range, 'value'))

  # Create a colorbar widget
  colorbar = ColorBar(colored_mesh)

  # Colormap choice widget
  colormap = Dropdown(
      options=colormaps,
      description='colormap:'
  )

  jslink((colored_mesh, 'colormap'), (colormap, 'index'))

  AppLayout(
      header=Scene([colored_mesh]),
      left_sidebar=VBox((colormap, colormap_slider_range)),
      right_sidebar=(colorbar),
      pane_widths=[1, 0, 1],
      pane_heights=['80','20',0],
      footer=None,
  )
```


```{Tip}
The benchmark geometry shown above is interactive and shows $u_x$ in [m].
```

```{figure} .   /sketch.png
---
width: 400px
alt: Hemispherical shell point load benchmark
name: Hemispherical shell point load benchmark
---
Hemispherical shell point load benchmark
```

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property               | Value                | Unit       |
|------------------------|----------------------|------------|
| Young's modulus, E     | $68.25 \cdot 10^{9}$ | Pa         |
| Poisson's ratio, $\nu$ | 0.3                  | -          |

## Boundary conditions

- symmetry along edge AE,
- symmetry along edge CE,
- $u_x=u_y=u_z=0$ at point E.
## Loading
- radial outward force of 2000 N at point A,
- radial inward force of 2000 N at point C,
