# Model setup

## Model definition

The Raasch challenge test has been proposed by Knight to benchmark linear shell models where drill rotations, for example shell in-plane rotations, play an important role. Within this study, a distributed force is applied at the edge of the free edge, so that the displacement of 0.125 m is expected in Z direction.

It should be noted that the original Raasch challenge benchmark has been modeled with Imperial units. In this particular study, the units have been converted into SI units (m, N, Pa, kg).

```{jupyter-execute}
:hide-code:
import numpy as np
import pyvista as pv
from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink, Layout, VBox, HBox
from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps

mesh = TetraMesh.from_vtk('benchmarks/007-raasch-challenge/elmer.vtu', show_edges = True)

dispy_min = 0.0
dispy_max = 0.125

# Colorize by height
colored_mesh = IsoColor(mesh, input=('u','X3'), min=dispy_min, max=dispy_max)

# Create a slider that will dynamically change the boundaries of the colormap
colormap_slider_range = FloatRangeSlider(value=[dispy_min, dispy_max], min=dispy_min, max=dispy_max, step=(dispy_max - dispy_min) / 100.)

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
The benchmark geometry shown above is interactive and it shows displacement in horizontal direction [m].
```

```{figure} .   /raasch.png
---
width: 400px
alt: Raasch challenge test
name: Raasch challenge test
---
<<<<<<< HEAD
Sketch of the Raasch challenge test (width=0.508m)
=======
Sketch of the Raasch challenge test
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
```

## Target solution

As per the [source](https://www.code-aster.org/V2/doc/v12/en/man_v/v3/v3.03.119.pdf), displacement of 0.125 m in Z direction is the target solution for the presented study.

## Material properties

| Property              | Value                | Unit       |
|-----------------------|----------------------|------------|
| Young's modulus, E    | 22752510             | Pa         |
| Poissons ratio, $\nu$ | 0.35                 | -          |

## Boundary conditions

The movement of the shell presented in this study is restrained in all directions at its' left side.

The model is driven by the distributed force of 8.7594 N/m applied to the model free edge.