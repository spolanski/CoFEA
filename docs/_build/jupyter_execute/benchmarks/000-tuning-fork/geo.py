#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ipygany import Scene, TetraMesh

mesh = TetraMesh.from_vtk('benchmarks/000-tuning-fork/fork.vtk')


scene = Scene([mesh])
scene

