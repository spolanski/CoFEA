#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ipygany import Scene, TetraMesh, IsoColor

mesh = TetraMesh.from_vtk('benchmarks/001-LE10-THICK-PLATE/elipse.vtu')



scene = Scene([mesh])
scene

