#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pyvista as pv
from ipywidgets import FloatSlider, FloatRangeSlider, Dropdown, Select, Box, AppLayout, jslink
from ipygany import Scene, IsoColor, TetraMesh, Component, ColorBar, colormaps



mesh = TetraMesh.from_vtk('benchmarks/001-thick-plate/elipse.vtu', show_edges = True)

sigmayy_min = -1.5e7
sigmayy_max = 1.5e7

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
    center=Scene([colored_mesh]),
    header=Box((colormap, colorbar)),
    footer=Box((colormap_slider_range,)),
    pane_heights=['10%', 1, '10%'],
    justify_content='center',
    align_content='center',
)

