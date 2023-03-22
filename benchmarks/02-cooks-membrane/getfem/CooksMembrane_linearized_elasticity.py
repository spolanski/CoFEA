#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
# This script implements the linearized elasticity Cook's membrane benchmark
# based on GetFEM  
#
# Copyright (C) 2023 Konstantinos Poulios
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#############################################################################
import getfem as gf
gf.util_trace_level(1)

# Input data
L = 48.           # block length
H1 = 44.          # block height
H2 = 16.

N_L = 2        # number of elements in block length direction
N_H = 2        # number of elements in block height direction

E = 70.
nu = 1./3. # 0.4999

traction = 6.25    # N/mm²  

#------------------------------------
geotrans = "GT_QK(2,2)"  # geometric transformation
#geotrans = "GT_Q2_INCOMPLETE(2)"

disp_fem_order = 2     # displacements finite element order
integration_degree = 5 # 9 gauss points per quad
#------------------------------------

# mesh regions
L_BOUNDARY = 3
R_BOUNDARY = 4

mesh = gf.Mesh("import", "structured",
               f"GT='{geotrans}';ORG=[0,{-H1}];SIZES=[{L},{H1}];NSUBDIV=[{N_L},{N_H}]")
mesh.set_region(L_BOUNDARY, mesh.outer_faces_with_direction([-1,0], gf.numpy.pi/10))
mesh.set_region(R_BOUNDARY, mesh.outer_faces_with_direction([1,0], gf.numpy.pi/10))

pts = mesh.pts()
for i in range(pts.shape[1]):
   x,y = pts[:,i]
   pts[1,i] += x/L*(H2*(y/H1+1)-y)
mesh.set_pts(pts)

# FEM
mfu = gf.MeshFem(mesh, 2)
mfu.set_classical_fem(disp_fem_order)
#mfu.set_fem(gf.Fem("FEM_Q2_INCOMPLETE(2)"))

mfout = gf.MeshFem(mesh)
mfout.set_classical_discontinuous_fem(disp_fem_order)

mim = gf.MeshIm(mesh, integration_degree)

# Model
md = gf.Model("real")
md.add_fem_variable("u", mfu)        # displacements
md.add_initialized_data("traction", traction)
md.add_initialized_data("LAMBDA", E*nu/((1+nu)*(1-2*nu)))
md.add_initialized_data("MU", E/(2*(1+nu)))
md.add_macro("sigma", "LAMBDA*Div(u)*Id(2)+MU*(Grad_u+Grad_u')")
md.add_linear_term(mim, "sigma:Grad_Test_u")
md.add_linear_term(mim, "-traction*Test_u(2)", R_BOUNDARY)
md.add_Dirichlet_condition_with_multipliers(mim, "u", mfu, L_BOUNDARY)
print(f"Displacement dofs: {mfu.nbdof()}\nTotal model dofs: {md.nbdof()}")

md.solve("noisy", "lsolver", "mumps")
VM = gf.linsolve_mumps\
  (gf.asm_mass_matrix(mim, mfout),
   gf.asm_generic(mim, 1, "sqrt(3/2)*Norm(Deviator(sigma))*Test_t", -1, md,
                  "t", True, mfout, gf.numpy.zeros(mfout.nbdof()), "select_output", "t")).T
mfout.export_to_vtu("CooksMembrane_linearized_elasticity.vtu",
                    mfu, md.variable("u"), "displacements",
                    mfout, VM, "Von Mises")
