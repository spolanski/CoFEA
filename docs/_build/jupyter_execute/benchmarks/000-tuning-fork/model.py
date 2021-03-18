#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("hello world")
get_ipython().run_line_magic('from', 'ipygany import Scene, TetraMesh')
get_ipython().run_line_magic('mesh', "= TetraMesh.from_vtk('benchmarks/000-tuning-fork/fork.vtk')")
get_ipython().run_line_magic('scene', '= Scene([mesh])')
get_ipython().run_line_magic('scene', '')

