import os
import meshpresso as msh
import copy

dir_path = os.path.dirname(os.path.realpath(__file__))
directory = dir_path + '/samples/'

def test_convert_to_inp():
    for filename in os.listdir(directory):
        if filename.endswith(".db"): 
            db_file = os.path.join(directory, filename)
            imp_mesh = msh.Mesh.import_from_db_file(path_to_db_file=db_file)
            imp_mesh.export_to_calculix(exported_filename=db_file.replace('.db', '.inp'))

def test_convert_to_unv():
    directory = dir_path + '/samples/'
    for filename in os.listdir(directory):
        if filename.endswith(".db"): 
            db_file = os.path.join(directory, filename)
            imp_mesh = msh.Mesh.import_from_db_file(path_to_db_file=db_file)
            imp_mesh.export_to_unv_format(exported_filename=db_file.replace('.db', '.unv'))

def test_simple_mesh_creation():
    # example: prepare db file from scratch
    # prepare nodes
    n1 = msh.Node(n_label=1, n_coords=(1.0, 0.0, 0.0))
    n2 = msh.Node(n_label=2, n_coords=(0.0, 1.0, 0.0))
    n3 = msh.Node(n_label=3, n_coords=(0.0, 0.0, 1.0))
    # put nodes into the list
    node_list = [n1, n2, n3]
    # prepare elements
    e1 = msh.Element(el_type='C3D4', el_label=1,
                       el_connect=(0, 1, 2),
                       part_all_nodes=node_list)
    # put elements into the list
    element_list = [e1, ]
    # create part from nodes and elements
    part = msh.PartMesh(part_name='test_part',
                          part_nodes=node_list,
                          part_elements=element_list)
    # put parts into the list
    part_dict = {'test_part': part}
    # create a model
    model = msh.Mesh(model_name='test',
                     dict_of_parts=part_dict)
    # save it to db file
    model.save_to_db_file(directory + 'simple.db')
    
    # example: load mesh from db file
    m = msh.Mesh.import_from_db_file(path_to_db_file=directory + 'simple.db')
    # the file is overwritten so if both export to calculix and unv is needed
    # then it has to be temporary stored somewhere
    copy_m = copy.deepcopy(m)
    m.export_to_calculix(exported_filename=directory + 'simple_ccx.inp')
    copy_m.export_to_unv_format(exported_filename=directory + 'simple_salome.unv')
    
if __name__ == '__main__':
    test_convert_to_inp()
    test_convert_to_unv()
    test_simple_mesh_creation()