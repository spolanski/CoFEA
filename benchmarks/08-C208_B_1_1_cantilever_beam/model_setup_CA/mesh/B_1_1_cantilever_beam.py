"""
Install gmsh acc. to https://pypi.org/project/gmsh/

"""
import os

import gmsh
import numpy as np

def get_line_length(vector):
    """
    Function uses output from 'gmsh.model.get_bounding_box(1, curve_id)' used
    on line and return its absolute length
    e.g.:
    input_vec = gmsh.model.get_bounding_box(1, curve_tag[1])
    line_length = get_line_length(input_vec)
    """
    dx = vector[0] - vector[3]
    dy = vector[1] - vector[4]
    dz = vector[2] - vector[5]
    
    return np.sqrt(dx**2+dy**2+dz**2)

if __name__ == "__main__":
    # Characteristic values
    beam_length = 3000
    beam_height = 480.0
    beam_width = 300.0

    element_length = 16.0*1
    
    # Gmsh initialization
    gmsh.initialize()
    gmsh.model.add("cantilever_beam")

    # Add points to model
    point_1 = gmsh.model.geo.addPoint(0.0, 0.0, 0, 0)
    point_2 = gmsh.model.geo.addPoint(0.0, beam_height, 0, 0)
    point_3 = gmsh.model.geo.addPoint(0.0, 0.0, beam_width / 2, 0)
    point_4 = gmsh.model.geo.addPoint(0.0, 0.0, -beam_width / 2, 0)
    
    # Create lines
    line_1 = gmsh.model.geo.addLine(point_1, point_2)
    line_2 = gmsh.model.geo.addLine(point_3, point_1)
    line_3 = gmsh.model.geo.addLine(point_1, point_4)

    # Execute
    gmsh.model.geo.synchronize()

    # Extrude lines
    extruded_featues = gmsh.model.geo.extrude(
        [*gmsh.model.getEntities(1)], beam_length, 0, 0
    )
    extruded_faces = list(filter(lambda x: x[0] == 2, extruded_featues))

    # Execute extrusion
    gmsh.model.geo.synchronize()

    # Physical groups - lines
    restraint_lines = gmsh.model.getEntitiesInBoundingBox(
        0 - 1,
        0 - 1,
        -beam_width * 0.5 - 1,
        0 + 1,
        beam_height + 1,
        beam_width * 0.5 + 1,
        1,
    )
    restraint = gmsh.model.addPhysicalGroup(
        1, list(map(lambda x: x[1], restraint_lines))
    )
    gmsh.model.setPhysicalName(1, restraint, "restraint")

    forces_lines = gmsh.model.getEntitiesInBoundingBox(
        beam_length - 1,
        0 - 1,
        -beam_width * 0.5 - 1,
        beam_length + 1,
        beam_height + 1,
        beam_width * 0.5 + 1,
        1,
    )
    force = gmsh.model.addPhysicalGroup(1, list(map(lambda x: x[1], forces_lines)))
    gmsh.model.setPhysicalName(1, force, "force")

    # Physical groups - surfaces
    vertical_plate = gmsh.model.getEntitiesInBoundingBox(
        0 - 1,
        0 - 1,
        0 - 1,
        beam_length + 1,
        beam_height + 1,
        0 + 1,
        2,
    )
    
    vertical_plate = gmsh.model.addPhysicalGroup(2, list(map(lambda x: x[1], vertical_plate)))
    gmsh.model.setPhysicalName(2, vertical_plate, "vertical_plate")

    horizontal_plate = gmsh.model.getEntitiesInBoundingBox(
        0 - 1,
        0 - 1,
        -beam_width/2 - 1,
        beam_length + 1,
        0+1,
        beam_width/2 + 1,
        2,
    )
    
    horizontal_plate = gmsh.model.addPhysicalGroup(2, list(map(lambda x: x[1], horizontal_plate)))
    gmsh.model.setPhysicalName(2, horizontal_plate, "horizontal_plate")


    point_aux = gmsh.model.geo.addPoint(beam_length, 58.6, 0)
    aux_point = gmsh.model.addPhysicalGroup(0, (0,point_aux))
    gmsh.model.setPhysicalName(0, aux_point, "aux_point")


    # Synchonization
    gmsh.model.geo.synchronize()

    # Mesh
    for curve_tag in gmsh.model.getEntities(1):
        # Get coordinates of start and end points of curve
        input_vec = gmsh.model.get_bounding_box(1, curve_tag[1])
        # Calculate lines length
        line_length = get_line_length(input_vec)
        # Number of nodes 
        number_of_nodes = int(line_length / element_length)
        # Set number of nodes on line
        gmsh.model.mesh.setTransfiniteCurve(curve_tag[1], number_of_nodes)

    for surf_tag in gmsh.model.getEntities(2):
        # Set structured scheme on surface        
        gmsh.model.mesh.setTransfiniteSurface(surf_tag[1])
        # Set quadrangle mesh on surface
        gmsh.model.mesh.setRecombine(2, surf_tag[1])

    # Generate mesh
    gmsh.model.mesh.generate(2)
    # Save mesh
    gmsh.write("B_1_1_cantilever_beam.med")
    # Save .geo file
    gmsh.write("B_1_1_cantilever_beam.geo_unrolled")
    # Run gmsh window
    gmsh.fltk.run()
    # Close gmsh session
    gmsh.finalize()
