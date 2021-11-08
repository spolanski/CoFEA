# Model setup

## Model definition

The aim of this study is to compare the results from a static analysis performed in [CalculiX](http://www.calculix.de/), [Code_Aster](https://code-aster.org/) and [Elmer](http://www.elmerfem.org/blog/) Finite-Element codes. Hertz contact geometry  will be used to measure the software performance. The aim of this benchmark is to examine the $\tau_{max}$ of the model equal of 502MPa. The highest von Mises stresses should be found in z equal to 0,2374mm.

Simulation input files used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/03-Hertz-contact)!

```{jupyter-execute}
:hide-code:
import numpy as np
import pyvista as pv
from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink, Layout, VBox, HBox
from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps

mesh = TetraMesh.from_vtk('benchmarks/003-Hertz-contact/very-fine-quad-hex.vtu', show_edges = True)

stress_min = 0.0
stress_max = 934

# Colorize by height
colored_mesh = IsoColor(mesh, input=('S','Mises'), min=stress_min, max=stress_max)

# Create a slider that will dynamically change the boundaries of the colormap
colormap_slider_range = FloatRangeSlider(value=[stress_min, stress_max], min=stress_min, max=stress_max, step=(stress_max - stress_min) / 100.)

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
The benchmark geometry shown above is interactive and it shows von Mises Stress [MPa].
```

```{figure} .   /sketch.png
---
width: 400px
alt: Hertz contact model
name: Hertz contact model
---
Sketch of the Hertz contact model
```

## Target solution

 $\tau_{max}$= 502 MPa and highest von Mises stresses at point y = 0,2374mm are expected

## Material properties

| Property              | Value                | Unit       |
|-----------------------|----------------------|------------|
| Young's modulus, E    | 20000000             | Pa         |
| Poissons ratio, $\nu$ | 0.30                 | -          |

## Boundary conditions

- symmetry along vertical axis,
- symmetry along horizontal axis.

## Loading
-pressure of 10MPa along horizontal lower edge of block,
