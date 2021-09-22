#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

