#!/usr/bin/env python
"""
Script for running in salome to automatically create regular mesh for thick_plate_benchmark

Change PATH_TO_EXPORT_MESH to your own path.
You can also change MESH_MULTIPLIER to make mesh more or less dense.
"""

###
### SALOME v9.3.0
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


# First parameter argv[0] is the current path
print("###")
PATH_TO_EXPORT_MESH = sys.argv[1] # "/home/filon/Desktop/"
print(f"PATH_TO_EXPORT_MESH: {PATH_TO_EXPORT_MESH} type:{type(PATH_TO_EXPORT_MESH)}")
MESH_MULTIPLIER = int(sys.argv[2]) 	# 10
print(f"MESH_MULTIPLIER: {MESH_MULTIPLIER} type: {type(MESH_MULTIPLIER)} ")
regular_mesh = sys.argv[3] 		# = True
print(f"regular_mesh: {regular_mesh} type:{type(regular_mesh)}")
linear_elements = sys.argv[4] 	# True
print(f"linear_elements: {linear_elements} type:{type(linear_elements)}")
print("###")

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )


##############################################
# Create vertices
points={}
coors_list = [(0, 1, 0),(0, 2.75, 0),(3.25, 0, 0),(2, 0, 0)]
for coors, point_name in zip(coors_list, ["Ap", "Bp", "Cp","Dp"]) :
	points[f"{point_name}"] = geompy.MakeVertex(*coors)

for point_key, new_point_name in zip(["Ap", "Bp", "Cp","Dp"], ["A", "B", "C","D"]):
	points[new_point_name] = geompy.TranslateDXDYDZ(points[point_key], 0, 0, 0.6, theCopy=True)
	geompy.addToStudy( points[new_point_name] , new_point_name)

for point_key, new_point_name in zip(["Ap", "Bp", "Cp","Dp"], ["Fp", "Ep", "E","F"]):
	points[f"{new_point_name}"] = geompy.TranslateDXDYDZ(points[point_key], 0, 0, 0.3, theCopy=True)
	geompy.addToStudy( points[f"{new_point_name}"] , f"{new_point_name}")

points["E"] = geompy.TranslateDXDYDZ(points["Cp"], 0, 0, 0.3, theCopy=True)
points["Ep"] = geompy.TranslateDXDYDZ(points["Bp"], 0, 0, 0.3, theCopy=True)

# Create lines
lines = {}
lines["Ap_Bp"] = geompy.MakeLineTwoPnt(points["Ap"], points["Bp"])
lines["Bp_Cp"] = geompy.MakeArcOfEllipse(O, points["Bp"], points["Cp"])
lines["Cp_Dp"] = geompy.MakeLineTwoPnt(points["Cp"], points["Dp"])
lines["Dp_Ap"] = geompy.MakeArcOfEllipse(O, points["Dp"], points["Ap"])

# Create faces
faces = {}
faces["f1"] = geompy.MakeFaceWires([lines["Ap_Bp"], lines["Bp_Cp"], lines["Cp_Dp"], lines["Dp_Ap"]], 1)
faces["f2"] = geompy.TranslateDXDYDZ(faces["f1"], 0, 0, 0.3, theCopy=True)

# Create solids
solids = {}
solids["s1"] = geompy.MakePrismVecH(faces["f1"], OZ, 0.6)
solids["s2"] = geompy.MakePartition([solids["s1"]], [faces["f2"]], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

# Add objects to GUI
for key, val in points.items():
	geompy.addToStudy( val, key )
for key, val in lines.items():
	geompy.addToStudy( val, key )
for key, val in faces.items():
	geompy.addToStudy( val, key )
for key, val in solids.items():
	geompy.addToStudy( val, key )


# Create groups of vertices
vertices = {}
group_vertices = {}
for key, val in points.items():
	vertices[key] = geompy.GetVertexNearPoint( solids["s2"], val)
	group_vertices[key] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["VERTEX"], key )
	geompy.UnionList( group_vertices[key], [vertices[key]])

# Create group of edges (to create mesh)

pairs = {
	"d1": [("A", "B"), ("Fp", "Ep"), ("Ap", "Bp"), ("D", "C"), ("F", "E"), ("Dp", "Cp")],
	"d2e": [("B", "C"), ("Ep", "E"), ("Bp", "Cp")],
	"d2i": [("A", "D"), ("Fp", "F"), ("Ap", "Dp")],
	"d3": [("Ap", "Fp"), ("Fp", "A"), ("Bp", "Ep"), ("Ep", "B"), ("Dp", "F"), ("F", "D"), ("Cp", "E"), ("E", "C")],
	"Uz": [("E", "Ep"),]
}
groups_edges = {}
for key in pairs.keys():
	list_entities = []
	for vertex_1, vertex_2 in pairs[key]:
		list_entities.append(geompy.GetEdge(solids["s2"], vertices[vertex_1], vertices[vertex_2]))
	groups_edges[key] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["EDGE"], key )
	geompy.UnionList( groups_edges[key] , list_entities)


group_of_faces = {}
# Create group of face to pressure
handle = geompy.GetFaceByPoints(solids["s2"], vertices["A"], vertices["B"], vertices["C"], vertices["D"])
group_of_faces["Pressure"] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["FACE"], "Pressure" )
geompy.UnionList( group_of_faces["Pressure"], [handle])

# Create group of face to Uy
handle_1 = geompy.GetFaceByPoints(solids["s2"], vertices["Dp"], vertices["Cp"], vertices["E"], vertices["F"])
handle_2 = geompy.GetFaceByPoints(solids["s2"], vertices["F"], vertices["E"], vertices["C"], vertices["D"])
group_of_faces["Uy"] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["FACE"], "Uy" )
geompy.UnionList( group_of_faces["Uy"], [handle_1, handle_2])

# Create group of face to Ux
handle_1 = geompy.GetFaceByPoints(solids["s2"], vertices["A"], vertices["B"], vertices["Ep"], vertices["Fp"])
handle_2 = geompy.GetFaceByPoints(solids["s2"], vertices["Fp"], vertices["Ep"], vertices["Bp"], vertices["Ap"])
group_of_faces["Ux"] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["FACE"], "Ux" )
geompy.UnionList( group_of_faces["Ux"], [handle_1, handle_2])

# Create group of face to UxUy
handle_1 = geompy.GetFaceByPoints(solids["s2"], vertices["Cp"], vertices["E"], vertices["Ep"], vertices["Bp"])
handle_2 = geompy.GetFaceByPoints(solids["s2"], vertices["E"], vertices["C"], vertices["B"], vertices["Ep"])
group_of_faces["UxUy"] = geompy.CreateGroup( solids["s2"], geompy.ShapeType["FACE"], "UxUy" )
geompy.UnionList( group_of_faces["UxUy"], [handle_1, handle_2])


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()

mesh_s2 = smesh.Mesh(solids["s2"])

# Mesh faces and solids
if regular_mesh == "True":
	Quadrangle_2D = mesh_s2.Quadrangle(algo=smeshBuilder.QUADRANGLE)
	Hexa_3D = mesh_s2.Hexahedron(algo=smeshBuilder.Hexa)
elif regular_mesh == "False":
	NETGEN_2D = mesh_s2.Triangle(algo=smeshBuilder.NETGEN_2D)
	NETGEN_3D = mesh_s2.Tetrahedron()
else:
	raise Exception("Bad 'regular_mesh' parameter")



Regular_1Da = mesh_s2.Segment(geom=groups_edges["d1"]).NumberOfSegments(2*MESH_MULTIPLIER)
Regular_1Db = mesh_s2.Segment(geom=groups_edges["d2e"]).NumberOfSegments(3*MESH_MULTIPLIER)
Regular_1Dc = mesh_s2.Segment(geom=groups_edges["d2i"]).NumberOfSegments(3*MESH_MULTIPLIER)
Regular_1Dd = mesh_s2.Segment(geom=groups_edges["d3"]).NumberOfSegments(1*MESH_MULTIPLIER)

mesh_s2.Compute()

if linear_elements == "False":
	mesh_s2.ConvertToQuadratic(0)
elif linear_elements == "True":
	pass
else:
	raise Exception("Bad 'linear_elements' parameter")

# Rename groups to be consistent with bechmark meshes
# Create groups of entities on mesh and use name to be consistent with bechmark meshes
mesh_s2.GroupOnGeom(group_of_faces["Pressure"], "E_2_DIST", SMESH.FACE)
mesh_s2.GroupOnGeom(group_of_faces["Uy"], "N_4_DC", SMESH.FACE)
mesh_s2.GroupOnGeom(group_of_faces["Ux"], "N_2_AB", SMESH.FACE)
mesh_s2.GroupOnGeom(group_of_faces["UxUy"], "N_3_BC", SMESH.FACE)
mesh_s2.GroupOnGeom(groups_edges["Uz"],'N_9_MID',SMESH.EDGE)


# Export mesh
mesh_s2.ExportUNV(PATH_TO_EXPORT_MESH + 'UserMesh.unv')
