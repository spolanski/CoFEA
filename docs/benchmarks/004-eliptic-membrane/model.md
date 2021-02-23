# Model definition
## Benchmark aim

The aim of this study is to compare the results from a static analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. A thick plate geometry will be used to measure the software performance. The model described in this report was created on a basis of the article found in this [link](http://wufengyun.com:888/v6.14/books/bmk/ch04s02anf01.html).

The aim of this benchmark is to examine the stress $\sigma_{yy}$ of the membrane at the point D. The target solution at this point is expected to be equal to 92.7 MPa. Additionally, the benchmark allow to test how easy is to apply pressure load condition.

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/01-LE10-Thick-Plate)!

```{jupyter-execute}
:hide-code:
import numpy as np
import pyvista as pv
from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink, Layout, VBox, HBox
from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps



mesh = TetraMesh.from_vtk('benchmarks/004-eliptic-membrane/eliptic-membrane.vtu', show_edges = True)

sigmayy_min = -3.4e7
sigmayy_max = 9.3e7

# Colorize by height
colored_mesh = IsoColor(mesh, input=('S','YY'), min=sigmayy_min, max=sigmayy_max)

# Create a slider that will dynamically change the boundaries of the colormap
colormap_slider_range = FloatRangeSlider(value=[sigmayy_min, sigmayy_max], min=sigmayy_min, max=sigmayy_max, step=(sigmayy_max - sigmayy_min) / 100.)

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
    pane_heights=['80%','20%',0],
    footer=None,
)
```



```{Tip}
The benchmark geometry shown above is interactive and shows $\sigma_{yy}$ results in [Pa].
```

```{figure} .   /sketch.png
---
width: 600px
alt: Eliptic membrane benchmark
name: Eliptic membrane benchmark
---
Sketch of the eliptic membrane under pressure benchmark
```

## Material properties

The table below presents all the material properties that were used in the study. These properties aim to reproduce the behaviour of steel material.

| Property               | Value                | Unit       |
|------------------------|----------------------|------------|
| Density $\rho$         | $7800.0$             | kg/$m^{3}$ |
| Young's modulus, E     | $2.10 \cdot 10^{11}$ | Pa         |
| Poisson's ratio, $\nu$ | 0.3                  | -          |

## Boundary conditions

- $u_y=0$ on edge DC.
- $u_x=0$ on edge AB.

## Loading
- uniform normal pressure of 10.0 MPa on BC edge.
