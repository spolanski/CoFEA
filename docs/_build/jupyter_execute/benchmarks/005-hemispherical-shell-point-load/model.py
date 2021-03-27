#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    pane_heights=['80%','20%',0],
    footer=None,
)

