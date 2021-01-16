# _*_ coding: utf_8 _*_
"""
todo:
- check python3
- change to snake_case
"""
import meshpresso_misc as misc
from collections import defaultdict, OrderedDict
import pickle
import pprint
import os

file_path = os.path.dirname(os.path.realpath(__file__))
element_library = misc.ElementLibrary()

try:
    import jinja2
except ImportError:
    print('warning! jinja2 not available. it will not be possible to export mesh\n')

class Node(object):
    """used to create node objects from external data

    attributes
    ----------
    label: int
        node number
    coordinates: tuple
        node coordinates
    """

    def __init__(self, n_label, n_coords):
        """node class constructor.

        parameters
        ----------
        n_label: int
            node number
        n_coords: tuple
            node coordinates (x,y,z)
        """
        self.label = n_label
        self.coordinates = n_coords

    def __repr__(self):

        return 'nd_%d' % self.label

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.label == other.label)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())

    def change_label(self, new_label):
        """a function to change node label
        
        parameters
        ----------
        new_label: int
            new node number
        """
        self.label = new_label


class Element(object):
    """class used to store information about elements,
    theirs type, label and connection to nodes
    
    attributes
    ----------
    type: str
        element type (eg C3D4)
    label: int
        element number
    connectivity: list
        list of nodes that element is based on
    """
    
    def __init__(self, el_type, el_label, el_connect,
                 part_all_nodes):
        """element object constructor

        parameters
        ----------
        el_type: str
            type of the element
        el_label: int
            element number
        el_connect: list
            list of **indices** that will be used to retrieve
            node objects from list of all nodes
        part_all_nodes: list
            list of all node objects retrieved from the current part
        
        """
        print el_type
        self.type = element_library.convert_to_general(str(el_type))
        self.label = el_label
        self.connectivity = [part_all_nodes[c] for c in el_connect]

    def __repr__(self):
        return 'el_%d' % self.label

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.label == other.label)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())
    
    def change_label(self, new_label):
        """a function to change element label
        
        parameters
        ----------
        new_label: int
            new element number
        """
        self.label = new_label

    def get_node_labels(self):
        """function returns labels of nodes which building the element

        returns
        -------
        list
            list of integers describing node labels
        """
        return [n.label for n in self.connectivity]

    def get_calculix_el_surfaces(self, surf_nodes_labels, surf_side):
        # import variable from misc module
        ccx_surf_definiton = misc.ccx_surface_definiton
        # list of element faces which are part of surface definition
        element_faces_list = []
        # common values from two lists
        intersection = lambda x, y: [i for i in x if i in y]
        # calculix definition of element faces
        topology = self.type[0]
        el_surf_def = ccx_surf_definiton[topology]
        # if topology in ('solid_tet', 'solid_wedge', 'solid_hex'):
        for face, nodes_label_indices in el_surf_def.items():
            node_labels = map(lambda i: self.connectivity[i].label, nodes_label_indices)
            common_nodes = intersection(node_labels, surf_nodes_labels)
            if len(common_nodes) == len(node_labels):
                element_faces_list.append(face)
        return element_faces_list

        
class PartMesh(object):
    """PartMesh is an object used to store mesh properties for a given part.

    attributes
    ----------
    name: str
        name of the part
    nodes: list of node objects
        list of the node objects
    elements: list
        list of the element objects
    elements_by_type: defaultdict(list)
        dictionary of elements grouped by element type
    el_set: defaultdict(list)
        dictionary of element sets grouped by element set name
    n_set: defaultdict(list)
        dictionary of node sets grouped by node set name
    surfaces : defaultdict(list), optional
        dictionary of surfaces {surf_name: {'nodes': n_set,
        'elements': el_set, 'sides': string},
        by default None
    """

    def __init__(self, part_name, part_nodes, part_elements,
                 element_sets=None, node_sets=None, surfaces=None):
        """PartMesh constructor

        parameters
        ----------
        part_name : str
            name of the part
        part_nodes : list
            list of node objects
        part_elements : list
            list of element objects
        element_sets : defaultdict(list), optional
            dictionary of elements sets {set_name: list of set elements},
            by default None
        node_sets : defaultdict(list), optional
            dictionary of node sets {set_name: list of set nodes},
            by default None
        surfaces : defaultdict(list), optional
            dictionary of surfaces {surf_name: {'nodes': n_set,
            'elements': el_set, 'sides': string},
            by default None
        """
        self.name = part_name
        self.nodes = part_nodes
        self.elements = part_elements
        self.elements_by_type = self.get_elements_by_type()
        
        if element_sets is None:
            self.el_set = defaultdict(list)
        else:
            self.el_set = element_sets
        if node_sets is None:
            self.n_set = defaultdict(list)
        else:
            self.n_set = node_sets
        if surfaces is None:
            self.surfaces = defaultdict(list)
        else:
            self.surfaces = surfaces
        
        self.ccx_el_set_surf_def = defaultdict(list)


    @classmethod
    def from_abaqus_cae(cls, abq_part):
        """function to initiate object from abaqus part.

        parameters
        ----------
        abq_part : abq_part
            abaqus part object

        returns
        -------
        part_mesh
            object containing part mesh definition
        """
        # define part name
        name = abq_part.name
        # create list of all nodes
        nodes = [Node(n.label, n.coordinates) for n in abq_part.nodes]
        # create list of all elements
        elements = [Element(e.type, e.label, e.connectivity,
                            nodes) for e in abq_part.elements]
        
        n_set = defaultdict(list)
        el_set = defaultdict(list)
        
        current_node_labels = [n.label for n in nodes]
        current_el_labels = [e.label for e in elements]
        
        for abq_set_name, abq_set_values in dict(abq_part.sets).items():
            # get labels from abaqus database
            node_label_list = [n.label for n in abq_set_values.nodes]
            # for each node get index from the list of current nodes
            list_of_indices = [current_node_labels.index(lab) for lab in node_label_list]
            # from list of indices get list of node objects
            list_of_nodes = [nodes[i] for i in list_of_indices]
            n_set['n_' + abq_set_name] = list_of_nodes

            element_label_list = [el.label for el in abq_set_values.elements]
            list_of_indices = [current_el_labels.index(lab)
                             for lab in element_label_list]
            list_of_elements = [elements[i] for i in list_of_indices]
            el_set['el_' + abq_set_name] = list_of_elements
        
        surfaces = defaultdict(list)
        for abq_surf_name, abq_surf_values in dict(abq_part.surfaces).items():
            node_label_list = [n.label for n in abq_surf_values.nodes]
            list_of_indices = [current_node_labels.index(lab) for lab in node_label_list]
            list_of_nodes = [nodes[i] for i in list_of_indices]
            list_of_unique_nodes = sorted(list(set(list_of_nodes)),
                                          key=lambda n: n.label)
            n_set['s_' + abq_surf_name] = list_of_unique_nodes

            element_label_list = [el.label for el in abq_surf_values.elements]
            list_of_indices = [current_el_labels.index(lab)
                             for lab in element_label_list]
            list_of_elements = [elements[i] for i in list_of_indices]
            list_of_unique_elements = sorted(list(set(list_of_elements)),
                                          key=lambda e: e.label)
            el_set['s_' + abq_surf_name] = list_of_unique_elements
            
            surfaces[abq_surf_name] = {'nodes': n_set['s_' + abq_surf_name],
                                     'elements': el_set['s_' + abq_surf_name],
                                     'sides': str(abq_surf_values.sides[0])}
        
        return cls(part_name=name, part_nodes=nodes, part_elements=elements,
                   element_sets=el_set, node_sets=n_set, surfaces=surfaces)

    def __str__(self):
        return pprint.pformat(self.__dict__, width=2)
    
    def __repr__(self):
        return 'part_%s' % self.name

    def get_nodes_from_label_list(self, label_list):
        """function to retrieve the nodes from list of node labels

        parameters
        ----------
        label_list: list
            list of integers describing node labes

        returns
        -------
        list
            list of node objects
        """
        current_labels = [n.label for n in self.nodes]
        list_of_indices = [current_labels.index(lab) for lab in label_list]
        list_of_nodes = [self.nodes[i] for i in list_of_indices]
        return list_of_nodes

    def get_elements_from_label_list(self, label_list):
        """function to retreive the elements from list of
        elements labels.

        parameters
        ----------
        label_list: list
            list of integers referring to element labels

        returns
        -------
        list
            list of element objects
        """
        current_labels = [e.label for e in self.elements]
        list_of_indices = [current_labels.index(lab) for lab in label_list]
        list_of_elements = [self.elements[i] for i in list_of_indices]
        return list_of_elements
    
    def get_elements_by_type(self):
        """function used to create a dictionary of elements with
        element types used as keys
        
        returns
        -------
        defaultdict(list)
            dictionary of elements with elementtypes used as keys
        """
        element_by_type = defaultdict(list)
        for e in self.elements:
            element_by_type[e.type].append(e)
        
        return element_by_type
    
    def renumber_nodes(self, new_label_list):
        # range_of_labels = xrange(start_label, len(self.nodes) + start_label)
        map(lambda node, new_lab: node.change_label(new_lab), self.nodes, new_label_list)
    
    def renumber_elements(self, new_label_list):
        # range_of_labels = xrange(start_label, len(self.nodes) + start_label)
        map(lambda element, new_lab: element.change_label(new_lab), self.elements, new_label_list)
        

    def set_element_type_format(self, new_format):
        """function to change element types in dictionary
        elements_by_type (for example from c3_d20_r to 116)

        parameters
        ----------
        new_format : str
            new format (eg 'UNV')
        """
        # create a temporary dict
        temp_element_by_type = defaultdict(list)
        # iterate over all element types in the dict
        for el_type_name, el_values in self.elements_by_type.items():
            # get new format for each type fo element
            new_el_type = element_library.convert_to_specific_format(general_format=el_type_name,
                                                                     output=new_format)
            # new_el_type = self.get_diff_format_for_el_type(old_el_type=el_type_name,
            #                                         new_mesh_format=new_format)
            temp_element_by_type[new_el_type] = el_values
        # swap temporary dict with dict with new formats
        self.elements_by_type = temp_element_by_type
    
    def reorder_nodes_in_el_definition(self, mesh_format):
        """function used to reoder nodes. by default the node
        order is the same as in abaqus.

        parameters
        ----------
        mesh_format : str
            format of mesh to be converted to
        """
        # c3_d20_r
        # abq = [5, 6, 8, 7, 1, 2, 4, 3, 12, 11,
        #        10, 9, 13, 14, 15, 16, 18, 17, 19, 20]
        # unv = [5, 12, 6, 11, 8, 10, 7, 9, 18, 17, 19,
        #        20, 1, 13, 2, 14, 4, 15, 3, 16]
        # c3_d10
        # abq = [4, 3, 1, 2, 7, 6, 5, 9, 8, 10]
        # unv = [4, 7, 3, 6, 1, 5, 9, 8, 10, 2]
        # c3_d15
        # abq = [3, 2, 1, 6, 5, 4, 9, 8, 7, 10, 11, 12, 14, 13, 15]
        # unv = [3, 9, 2, 8, 1, 7, 14, 13, 15, 6, 10, 5, 11, 4, 12]
        # idx _ order to be used in function
        # idx = [abq.index(i) for i in unv]
        def change_order(elements, order):
            for el in elements:
                el.connectivity = [el.connectivity[i] for i in order]
        if mesh_format == 'UNV':
            for el_type, elements in self.elements_by_type.items():
                if '118' == el_type:
                    order = [0, 4, 1, 5, 2, 6, 7, 8, 9, 3]
                    change_order(elements, order)
                elif '113' == el_type:
                    order = [0, 6, 1, 7, 2, 8, 12, 13, 14,
                             3, 9, 4, 10, 5, 11]
                    change_order(elements, order)
                elif '116' == el_type:
                    order = [0, 8, 1, 9, 2, 10, 3, 11,
                             16, 17, 18, 19, 4, 12, 5,
                             13, 6, 14, 7, 15]
                    change_order(elements, order)


class Mesh(object):
    """Mesh is the most general class used to import, store
    and export mesh data. the idea is to initialise the constructor,
    then import mesh from db file. finally, the mesh can be
    exported to an external format. for example
    
    >>> mesh = Mesh()
    >>> mesh.import_from_db_file(path_to_db_file='mesh.db')
    >>> mesh.export_to_calculix(exported_filename='calculix.inp')
    >>> mesh.export_to_unv_format(exported_filename='salome.unv')
    
    attributes
    ----------
    model_name : string
        name of imported model
    parts : list
        list of imported parts
    assembly_mesh: dictionary
        the dictionary contains parts, but those have renumbered\
        node and element labels, so that the labels are not\
        repeating
    """

    coordinate_system = dict(part_UID = 1,
                             part_name = 'SMESH_Mesh',
                             label = 1,
                             type_ = 0,
                             color = 0,
                             name = 'Global Cartesian Coordinate System',
                             transf_matrix = [[1, 0, 0],
                                              [0, 1, 0],
                                              [0, 0, 1],
                                              [0, 0, 0]]
                        )

    def __init__(self, model_name, dict_of_parts, asbly_element_sets=None,
                 asbly_node_sets=None, asbly_surfaces=None):
        self.model_name = model_name
        self.parts = dict_of_parts

        # assembly element sets
        if asbly_element_sets is None:
            self.el_set = defaultdict(list)
        else:
            self.el_set = asbly_element_sets
        # assembly node sets
        if asbly_node_sets is None:
            self.n_set = defaultdict(list)
        else:
            self.n_set = asbly_node_sets
        # assembly surfaces
        if asbly_surfaces is None:
            self.surfaces = defaultdict(list)
        else:
            self.surfaces = asbly_surfaces

        self.renumber_mesh()
        self.ccx_el_set_surf_def = defaultdict(list)

    def __str__(self):
        if len(self.__dict__.keys()) == 0:
            return 'mesh object is empty. data needs to be loaded first'
        return pprint.pformat(self.__dict__, width=2)

    @classmethod
    def import_from_abaqus_cae(cls, abq_model_name, abq_root_assembly):
        """function to initiate the mesh object

        parameters
        ----------
        abq_model_name : str
            name of the abaqus model
        abq_part_list : list
            list of abaqus parts to export mesh from

        returns
        -------
        Mesh
            object containing model mesh definition
        """
        parts = OrderedDict((p.name, PartMesh.from_abaqus_cae(p))
                            for p in abq_root_assembly.allInstances.values()
                            if p.excludedFromSimulation is False)
        
        n_set = defaultdict(list)
        e_set = defaultdict(list)
        for set_name, set_values in abq_root_assembly.sets.items():
            if set_values.nodes:
                temp_dict = defaultdict(list)
                map(lambda n: temp_dict[n.instanceName].append(n.label), set_values.nodes)
                for inst, n_labels in temp_dict.items():
                    n_objects = parts[inst].get_nodes_from_label_list(label_list=n_labels)
                    n_set['n_' + set_name].extend(n_objects)
            if set_values.elements:
                temp_dict = defaultdict(list)
                map(lambda e: temp_dict[e.instanceName].append(e.label), set_values.elements)
                for inst, e_labels in temp_dict.items():
                    e_objects = parts[inst].get_elements_from_label_list(label_list=e_labels)
                    e_set['el_' + set_name].extend(e_objects)

        asbly_surfaces = defaultdict(list)
        for surf_name, surf_values in abq_root_assembly.surfaces.items():
            asbly_surfaces[surf_name] = defaultdict(list)
            temp_dict = defaultdict(list)
            map(lambda n: temp_dict[n.instanceName].append(n.label), surf_values.nodes)
            for inst, n_labels in temp_dict.items():
                n_objects = parts[inst].get_nodes_from_label_list(label_list=n_labels)
                asbly_surfaces[surf_name]['nodes'].extend(n_objects)
            
            temp_dict = defaultdict(list)
            map(lambda e: temp_dict[e.instanceName].append(e.label), surf_values.elements)
            for inst, e_labels in temp_dict.items():
                e_objects = parts[inst].get_elements_from_label_list(label_list=e_labels)
                asbly_surfaces[surf_name]['elements'].extend(e_objects)
            asbly_surfaces[surf_name]['sides'] = str(surf_values.sides[0])
            
        return cls(model_name=abq_model_name, dict_of_parts=parts,
                   asbly_element_sets=e_set, asbly_node_sets=n_set,
                   asbly_surfaces=asbly_surfaces)

    @classmethod
    def import_from_db_file(cls, path_to_db_file):
        """function to initiate the mesh object

        parameters
        ----------
        path_to_db_file : str
            path to the db file

        returns
        -------
        mesh
            object containing model mesh definition
        """
        with open(path_to_db_file, 'rb') as handle:
            mesh = pickle.load(handle)
        
        return cls(model_name=mesh['model_name'],
                   dict_of_parts=mesh['part_dict'],
                   asbly_element_sets=mesh['element_set'],
                   asbly_node_sets=mesh['node_set'],
                   asbly_surfaces=mesh['surfaces'])
    
    def save_to_db_file(self, name_of_db_file):
        """function to save model data to db file

        parameters
        ----------
        name_of_db_file : str
            name of the file that will be used to store data
        """
        dict_to_save = {'model_name': self.model_name,
                      'part_dict': self.parts,
                      'element_set': self.el_set,
                      'node_set': self.n_set,
                      'surfaces': self.surfaces,
                      }
        
        with open(name_of_db_file, 'wb') as handle:
            pickle.dump(dict_to_save, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
        print('mesh has been written into {0} file'.format(name_of_db_file))

    def renumber_mesh(self):
        """function computes mesh at assembly level from list
        of part objects. the returned dictionary contains
        parts with renumbered nodes and elements

        returns
        -------
        defaultdict(list)
            dictionary of parts
        """
        num_part_nodes = [len(part.nodes) for part in self.parts.values()]
        all_nodes = range(1, sum(num_part_nodes)+1)
        num_part_elements = [len(part.elements) for part in self.parts.values()]
        all_elements = range(1, sum(num_part_elements)+1)
        
        slice = lambda list, s: (list[:s], list[s:])
        
        new_numbering = []
        for nodes_len, elem_len in zip(num_part_nodes, num_part_elements):
            part_nodes, all_nodes = slice(all_nodes, nodes_len)
            part_elements, all_elements = slice(all_elements, elem_len)
            new_numbering.append((part_nodes, part_elements))
        
        for i, part in enumerate(self.parts.items()):
            part_name, part_value = part
            part_value.renumber_nodes(new_label_list=new_numbering[i][0])
            part_value.renumber_elements(new_label_list=new_numbering[i][1])

    def set_calculix_surf_definition(self, surface_source):
        """function converts part.surfaces into format appropriate
        for calculix.

        returns:
            dict: dictionary with surface name as keys and dictionary surface
            definition as value
        """
        # the idea below is to iterate over each surface definition and find
        # out what are the surface nodes and compare them with nodes from each
        # element defined in the surface. once compared it is possible to figure
        # out which face is used in the definition based on index of surf_node 
        # in element_node.
        # print dict(surface_source)
        # surface_source.ccx_el_set_surf_def = defaultdict(list)
        
        # for each surface define
        for surf_name, surf_value in surface_source.surfaces.items():
            # get node labels from surface definition
            node_labels = [n.label for n in surf_value['nodes']]
            # set temporary value
            temp_surface_definition = defaultdict(list)
            # for each element in surface definition
            for e in surf_value['elements']:
                # find list of pairs [(element, surface face),..]
                element_faces_list = e.get_calculix_el_surfaces(surf_nodes_labels=node_labels,
                                                           surf_side=surf_value['sides'])
                # add values to temporary surface dict
                map(lambda face : temp_surface_definition[face].append(e), element_faces_list)
            # for each item in {'el_face': [el_1, el_2,..]}
            for face, elements in temp_surface_definition.items():
                # create name set
                name_of_elset = 's_' + surf_name + '_' + face
                # add element set to surface_source for each face
                surface_source.el_set[name_of_elset] = elements
                # add apprioprate naming to temporary dict
                surface_source.ccx_el_set_surf_def[surf_name].append((name_of_elset, face))

    def export_to_calculix(self, exported_filename):
        """function to export mesh to calculix format

        parameters
        ----------
        exported_filename : str
            name of the file to export mesh (eg 'calculix.inp')
        """
        # get calculix/abaqus element format for each part
        for part in self.parts.values():
            # if any surface definition exists
            if len(part.surfaces.keys()):
                # compute surface definiton made with elements
                self.set_calculix_surf_definition(surface_source=part)
                # convert surface definition from elements to element sets
            part.set_element_type_format(new_format='CCX')

        self.set_calculix_surf_definition(surface_source=self)
        # prepare a dict which will be used to render things in template
        render_dict = {'model_name': self.model_name,
                      'parts': self.parts.values(),
                      'assembly_el_sets': self.el_set,
                      'assembly_n_sets': self.n_set,
                      'assembly_ccx_surfaces': self.ccx_el_set_surf_def}
        # load jinja template from file
        # https://stackoverflow.com/a/38642558
        template_loader = jinja2.FileSystemLoader(searchpath=file_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("calculix.tmplt")
        # render template with dict
        output_text = template.render(render_dict)
        # remove all empty lines
        output_text = '\n'.join([i for i in output_text.split('\n') if len(i)])
        output_text += '\n'
        # save input deck
        with open(exported_filename, 'w') as f:
            f.write(output_text)
        print('Mesh exported to {0}'.format(exported_filename))

    def export_to_unv_format(self, exported_filename):
        """function to export to unv format

        parameters
        ----------
        exported_filename : str
            name of the file to export mesh (eg 'salome.unv')
        """
        # get unv format for each part
        for part in self.parts.values():
            part.set_element_type_format(new_format='UNV')
            part.reorder_nodes_in_el_definition(mesh_format='UNV')
        # prepare a dict which will be used to render things in template
        render_dict = {'model_name': self.model_name,
                      'parts': self.parts.values(),
                      'assembly_el_sets': self.el_set,
                      'assembly_n_sets': self.n_set,
                      'coord_sys': self.coordinate_system,
                      }
        # render_dict = {'parts': self.parts}
        # load jinja template from file
        # https://stackoverflow.com/a/38642558
        template_loader = jinja2.FileSystemLoader(searchpath=file_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("unv.tmplt")
        # render template with dict
        output_text = template.render(render_dict)
        # remove all empty lines
        output_text = '\n'.join([i for i in output_text.split('\n') if len(i)])
        # save input deck
        with open(exported_filename, 'w') as f:
            f.write(output_text)
        print('Mesh exported to {0}'.format(exported_filename))
