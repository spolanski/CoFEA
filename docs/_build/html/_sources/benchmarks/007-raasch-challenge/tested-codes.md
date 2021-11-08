# Tested Finite Element codes

## CalculiX

The below section describes how the Raasch challenge model was created for Calculix solver. Although the model response does not give a correct result, the setup should still be provided in case someone would like to replicate the issue. As mentioned in the results section, in order to define distributed load over an edge a separate app called PrePoMax has to be used. This application converts distributed load definition into the set of nodal loads.

The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/07-Raasch-shell-challenge)

```
** # Material - material definition in Pa, m
*Material, Name=Material-1
*Elastic
22770000, 0.35

** # Section - shell thickness definition
*Shell section, Elset=S4R, Material=Material-1, Offset=0
0.0508

** # Step-1 - Static step definition
*Step
*Static

** # Boundary conditions definition
** # Name: Displacement fix
*Boundary, Fixed
fixedge, 1, 1
fixedge, 2, 2
fixedge, 3, 3

** # Loads definition
** # Name: Distributed load approximated with concentrated loads
*Cload
269, 3, 0.171084630782702
6, 3, 0.085542315391351
268, 3, 0.171084630782702
267, 3, 0.17108463073892
266, 3, 0.17108463073892
265, 3, 0.171084630782702
264, 3, 0.171084630782702
263, 3, 0.171084630782702
262, 3, 0.171084630782702
261, 3, 0.17108463073892
260, 3, 0.17108463073892
259, 3, 0.171084630782702
258, 3, 0.171084630782702
257, 3, 0.171084630782702
256, 3, 0.171084630782702
255, 3, 0.171084630782702
254, 3, 0.171084630738921
253, 3, 0.17108463073892
252, 3, 0.171084630782702
251, 3, 0.171084630782702
250, 3, 0.171084630773946
249, 3, 0.171084630765189
248, 3, 0.171084630769568
247, 3, 0.171084630769568
246, 3, 0.171084630769568
245, 3, 0.171084630769568
5, 3, 0.0855423153825947

** # Field outputs - output definition
*Node file
RF, U
*El file
S, E

** # End step
*End step
```

## Code_Aster

This section describes how the model has been set up in Code_Aster solver. As mentioned in the Results chapter, at the current stage of Code_Aster development it is not straightforward to postprocess second order type of element (QUAD8_9 and TRI6_7). This section describes how to achieve it

The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/07-Raasch-shell-challenge)
```
# Read mesh from UNV file
mesh = LIRE_MAILLAGE(FORMAT='IDEAS',
                     UNITE=2)

# Define quadratic element type
m_quad = CREA_MAILLAGE(MAILLAGE=mesh,
                       MODI_MAILLE=_F(OPTION='QUAD8_9',
                                      PREF_NOEUD='NS',
                                      TOUT='OUI'))

# Create shell definition for quadratic elements
pallet = AFFE_MODELE(AFFE=_F(MODELISATION=('COQUE_3D', ),
                             PHENOMENE='MECANIQUE',
                             TOUT='OUI'),
                     MAILLAGE=m_quad)

# Define shell thickness
elemprop = AFFE_CARA_ELEM(COQUE=_F(EPAIS=0.0508,
                                   GROUP_MA=('main', )),
                          MODELE=pallet)

# Define type of element section
# Notice that mesh, not m_quad variable is used
Postpro = AFFE_MODELE(AFFE=_F(MODELISATION=('3D', ),
                              PHENOMENE='MECANIQUE',
                              TOUT='OUI'),
                      MAILLAGE=mesh)

# Define material properties
mater = DEFI_MATERIAU(ELAS=_F(E=22770000.0,
                              NU=0.35))

# Assign material to the elements
materfl = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),
                                TOUT='OUI'),
                        MODELE=pallet)

# Define boundary conditions
mecabc = AFFE_CHAR_MECA(DDL_IMPO=_F(DRX=0.0,
                                    DRY=0.0,
                                    DRZ=0.0,
                                    DX=0.0,
                                    DY=0.0,
                                    DZ=0.0,
                                    GROUP_MA=('fixedge', )),
                        MODELE=pallet)

# Define distributed load
mecach = AFFE_CHAR_MECA(FORCE_ARETE=_F(FZ=8.7563,
                                       GROUP_MA=('load', )),
                        MODELE=pallet)

# Define result output 
result = MECA_STATIQUE(CARA_ELEM=elemprop,
                       CHAM_MATER=materfl,
                       EXCIT=(_F(CHARGE=mecabc),
                              _F(CHARGE=mecach)),
                       MODELE=pallet)

# Project the result from quadratic elements onto elements with central node 
PROJ = PROJ_CHAMP(MODELE_1=pallet,
                  MODELE_2=Postpro,
                  RESULTAT=result)

# Define a variable which will be printed to a text file
table = POST_RELEVE_T(ACTION=_F(GROUP_NO=('Disp', ),
                                INTITULE='DISP',
                                NOM_CHAM='DEPL',
                                OPERATION=('EXTRACTION', ),
                                RESULTANTE=('DZ', ),
                                RESULTAT=result))

# Define the results file with projected values
IMPR_RESU(FORMAT='MED',
          RESU=_F(RESULTAT=PROJ),
          UNITE=3)

# Define a text file where the extracted value will be printed
IMPR_TABLE(TABLE=table,
           UNITE=4)

```
## Elmer

The following section describes how to set up a model in Elmer software. The section also presents a structure of macro that can be run in FreeCAD

The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/07-Raasch-shell-challenge)

```
# Load mesh and define the path for the path
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/L_VF_T"
  Include Path ""
  Results Directory "Results/L_VF_T"
End

# Define type of simulation, CSYS and output file
Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Solver Input File = case.sif
  Post File = case.vtu
End

# Define constants
Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.670374419e-08
  Permittivity of Vacuum = 8.85418781e-12
  Permeability of Vacuum = 1.25663706e-6
  Boltzmann Constant = 1.380649e-23
  Unit Charge = 1.6021766e-19
End

# Assign material and section definition
Body 1
  Target Bodies(1) = 1
  Name = "Body 1"
  Equation = 1
  Material = 1
End

# Define shell solver definition
Solver 1
  Equation = "Shell equations"
  Procedure = "ShellSolver" "ShellSolver"
  Large Deflection = False
  Linear System Solver = Direct
  Linear System Preconditioning = ILU0
  Linear System Row Equilibration = Logical True
  Linear System Max Iterations = 1000
  Linear System Convergence Tolerance = 1e-8
  Linear System Direct Method = Umfpack
  Linear System GCR Restart = 300
  Linear System Abort Not Converged = False
  Steady State Convergence Tolerance = 1e-09
End

# Define solver to output displacement into the file
Solver 2 
  Equation = SaveScalars
  Procedure = "SaveData" "SaveScalars"
  Filename = results.dat
  Variable 1 = String u
  Operator 1 = String 3
  Save Points = 6
End

# Define shell behaviour
Equation 1
  Name = "ShellSolver"
  Active Solvers(1) = 1
End

# Define material properties
Material 1
  Name = "Material 1"
  Shell Thickness = 0.0508
  Poisson ratio = 0.35
  Youngs modulus = 22.77e6
End

# Define encastre conditions
Boundary Condition 1
  Target Boundaries(1) = 1 
  Name = "Fix"
  U 2 = 0
  U 3 = 0
  U 1 = 0
  DNU 3 = 0
  DNU 2 = 0
  DNU 1 = 0
End

# Define distributed load
Boundary Condition 2
  Target Boundaries(1) = 2 
  Name = "Force"
  Resultant Force 3 = Real 8.7563
End
```

```python
# -*- coding: utf-8 -*-
import FreeCAD
import Part
import numpy as np
from collections import defaultdict

import os
rootdir = '07-raasch-challenge/elmer/Mesh'

# The following script loops over all mesh.node files
# that can be found in rootdir
for subdir, dirs, files in os.walk(rootdir):
    for dir in dirs:
        mesh_name = rootdir + '/' + dir + '/mesh.nodes'
        with open(mesh_name, 'r') as f:
            # parse the file to obtain node & coordinate definition
            # then save the output to the dictionary coords
            nodes = f.read().split('\n')
            coords = defaultdict(list)
            for row in nodes[:-1]:
                node, t, c_x, c_y, c_z = row.split(' ')
                coords[node] = tuple([float(i) for i in [c_x, c_y, c_z]])

        # Open BREP file in FreeCAD
        Part.open(u"07-raasch-challenge/Raash.brep")

        txt = ''
        test = lambda f, pt: f.distToShape(pt)[0]
        shell_faces = App.ActiveDocument.Objects[0].Shape.Faces
        # the loop below goes over node and coordinates
        # then tries to compute normal vector for a given node
        # at the coordinate.
        for key, coord in coords.items():
            x, y, z = coord
            face = shell_faces
            p=Part.Point(App.Vector(x,y,z)).toShape()
            temp = [test(fe, p) for fe in face]
            min_dist_face = face[temp.index(min(temp))]
            face_surf = min_dist_face.Surface
            pt = FreeCAD.Base.Vector(x, y, z)
            uv = face_surf.parameter(pt)
            nv = min_dist_face.normalAt(uv[0], uv[1])
            nv = np.array(nv.normalize())
            txt += '{} {:.6f} {:.6f} {:.6f}\n'.format(key, nv[0], nv[1], nv[2])

        # the txt variable is printed into the mesh.director file
        with open(rootdir + '/' + dir + '/mesh.director','w') as f:
            f.write(txt)
```
