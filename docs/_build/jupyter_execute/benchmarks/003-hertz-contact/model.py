import numpy as np
import pyvista as pv
from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink, Layout, VBox, HBox
from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps

mesh = TetraMesh.from_vtk('benchmarks//003-hertz-contact/fine-quad-hex.vtu', show_edges = True)

vmises_min = 0.0
vmises_max = 940.0

# Colorize by height
colored_mesh = IsoColor(mesh, input=('S_Mises','S_Mises'), min=vmises_min, max=vmises_max)

# Create a slider that will dynamically change the boundaries of the colormap
colormap_slider_range = FloatRangeSlider(value=[vmises_min, vmises_max], min=vmises_min, max=vmises_max, step=(vmises_max - vmises_min) / 100.)

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