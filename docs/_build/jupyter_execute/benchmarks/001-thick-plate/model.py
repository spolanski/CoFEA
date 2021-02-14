#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ipygany import Scene, TetraMesh
mesh = TetraMesh.from_vtk('benchmarks/001-thick-plate/elipse.vtu')
scene = Scene([mesh])
scene

