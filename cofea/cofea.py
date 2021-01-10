# -*- coding: utf-8 -*-
"""
module authors:
- Slawomir Polanski
TODO:
- remove unnecesary comments
- check python3
- change to snake_case
- remove coordsys
- test unv
- keep only db files
- appropriate function order
"""
import meshpressoMisc as misc
from collections import defaultdict, OrderedDict
import pickle
import pprint
import os

filePath = os.path.dirname(os.path.realpath(__file__))
element_library = misc.ElementLibrary()
try:
    import jinja2
except ImportError:
    print('WARNING! jinja2 not available. It will not be possible to export mesh\n')

class CoordSys(object):
    """Class used to store coordinate system information.
    
    Attributes
    ----------    
    id: int
        Coordinate system number
    label: str
        Coordinate system name
    type: str
        Coordinate system type ('rec' - rectangular
                                'cyl' - cylindrical
                                'sph' - spherical)
    ref: int
        Reference coordinate system number
    origin: tuple
        Coordinate system origin specified in reference system (x,y,z)
    plus_x_point: tuple
        Coordinates of a point in the +x axis specified in reference
        system (x,y,z)
    plus_xz_points: tuple
        Coordinates of a point in the +xz axis specified in reference
        system (x,y,z)
    """

    def __init__(self, csID, csLabel, csType="rec", csRef=0, csOrigin=(0,0,0),
                 csPlusX=(1,0,0), csPlusXZ=(0,0,1)):
        """Coordinate system class constructor

        Parameters
        ----------
        csID: int
            Coordinate system number
        csLabel: str
            Coordinate system name
        csType: str
            Coordinate system type ('rec' - rectangular
                                    'cyl' - cylindrical
                                    'sph' - spherical)
        csRef: int
            Reference coordinate system number
        csOrigin: tuple
            Coordinate system origin specified in reference system (x,y,z)
        csPlusX: tuple
            Coordinates of a point in the +x axis specified in reference
            system (x,y,z)
        csPlusXZ: tuple
            Coordinates of a point in the +xz axis specified in
            reference system (x,y,z)
        """
        self.id = csID
        self.label = str(csLabel)
        self.type = str(csType)
        self.ref = csRef
        self.origin = csOrigin
        self.plus_x_point = csPlusX
        self.plus_xz_point = csPlusXZ

    def __repr__(self):
        return 'CSYS - ID: ' + str(self.id) + '; Label: ' + self.label

    def changeLabel(self, newLabel):
        """A function to change coordinate system label
        
        Parameters
        ----------
        newLabel: str
            New coordinate system label
        """
        self.label = str(newLabel)

    def changeID(self, newID):
        """A function to change coordinate system ID
            
        Parameters
        ----------
        newID: int
            New coordinate system ID
        """
        self.id = newID
            
class Node(object):
    """Used to create node objects from external data

    Attributes
    ----------
    label: int
        Node number
    coordinates: tuple
        Node coordinates
    csys: int
        Node coordinate system 
    """

    def __init__(self, nLabel, nCoords, nCSYS=0):
        """Node class constructor.

        Parameters
        ----------
        nLabel: int
            Node number
        nCoords: tuple
            Node coordinates (x,y,z)
        """

        self.label = nLabel
        self.coordinates = nCoords
        self.csys = nCSYS

    def __repr__(self):

        return 'ND-%d' % self.label

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.label == other.label)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())

    def changeLabel(self, newLabel):
        """A function to change node label
        
        Parameters
        ----------
        newLabel: int
            new node number
        """
        self.label = newLabel


class Element(object):
    """Class used to store information about elements,
    theirs type, label and connection to nodes
    
    Attributes
    ----------
    type: str
        element type (eg C3D4)
    label: int
        element number
    connectivity: list
        list of nodes that element is based on
    """
    
    def __init__(self, elType, elLabel, elConnect,
                 partAllNodes):
        """Element object constructor

        Parameters
        ----------
        elType: str
            type of the element
        elLabel: int
            element number
        elConnect: list
            list of **indices** that will be used to retrieve
            Node objects from list of all nodes
        partAllNodes: list
            list of all Node objects retrieved from the current part
        
        """
        self.type = element_library.convert_to_general(str(elType))
        self.label = elLabel
        self.connectivity = [partAllNodes[c] for c in elConnect]

    def __repr__(self):
        return 'EL-%d' % self.label

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.label == other.label)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())
    
    def changeLabel(self, newLabel):
        """A function to change element label
        
        Parameters
        ----------
        newLabel: int
            new element number
        """
        self.label = newLabel

    def getNodeLabels(self):
        """Function returns labels of nodes which building the element

        Returns
        -------
        list
            list of integers describing node labels
        """
        return [n.label for n in self.connectivity]

    def getCalculixElSurfaces(self, surfNodesLabels, surfSide):
        # import variable from misc module
        ccxSurfDefiniton = misc.ccxSurfaceDefiniton
        # list of element faces which are part of surface definition
        elementFacesList = []
        # common values from two lists
        intersection = lambda x, y: [i for i in x if i in y]
        # calculix definition of element faces
        topology = self.type[0]
        elSurfDef = ccxSurfDefiniton[topology]
        # if topology in ('SOLID-TET', 'SOLID-WEDGE', 'SOLID-HEX'):
        for face, nodesLindices in elSurfDef.items():
            nodeLabels = map(lambda i: self.connectivity[i].label, nodesLindices)
            commonNodes = intersection(nodeLabels, surfNodesLabels)
            if len(commonNodes) == len(nodeLabels):
                elementFacesList.append(face)
        return elementFacesList

        
class PartMesh(object):
    """PartMesh is an object used to store mesh properties for a given part.

    Attributes
    ----------
    name: str
        name of the part
    nodes: list of Node objects
        list of the Node objects
    elements: list
        list of the Element objects
    elementsByType: defaultdict(list)
        dictionary of elements grouped by element type
    elSet: defaultdict(list)
        dictionary of element sets grouped by element set name
    nSet: defaultdict(list)
        dictionary of node sets grouped by node set name
    surfaces : defaultdict(list), optional
        dictionary of surfaces {surfName: {'nodes': nSet,
        'elements': elSet, 'sides': string},
        by default None
    """

    def __init__(self, partName, partNodes, partElements,
                 elementSets=None, nodeSets=None, surfaces=None):
        """PartMesh constructor

        Parameters
        ----------
        partName : str
            name of the part
        partNodes : list
            list of Node objects
        partElements : list
            list of Element objects
        elementSets : defaultdict(list), optional
            dictionary of elements sets {setName: list of set elements},
            by default None
        nodeSets : defaultdict(list), optional
            dictionary of node sets {setName: list of set nodes},
            by default None
        surfaces : defaultdict(list), optional
            dictionary of surfaces {surfName: {'nodes': nSet,
            'elements': elSet, 'sides': string},
            by default None
        """
        self.name = partName
        self.nodes = partNodes
        self.elements = partElements
        self.elementsByType = self.getElementsByType()
        
        if elementSets is None:
            self.elSet = defaultdict(list)
        else:
            self.elSet = elementSets
        if nodeSets is None:
            self.nSet = defaultdict(list)
        else:
            self.nSet = nodeSets
        if surfaces is None:
            self.surfaces = defaultdict(list)
        else:
            self.surfaces = surfaces
        
        self.ccxElSetSurfDef = defaultdict(list)


    @classmethod
    def fromAbaqusCae(cls, abqPart):
        """Function to initiate object from Abaqus part.

        Parameters
        ----------
        abqPart : abqPart
            Abaqus part object

        Returns
        -------
        PartMesh
            object containing part mesh definition
        """
        # define part name
        name = abqPart.name
        # create list of all nodes
        nodes = [Node(n.label, n.coordinates) for n in abqPart.nodes]
        # create list of all elements
        elements = [Element(e.type, e.label, e.connectivity,
                            nodes) for e in abqPart.elements]
        
        nSet = defaultdict(list)
        elSet = defaultdict(list)
        
        currentNodeLabels = [n.label for n in nodes]
        currentElLabels = [e.label for e in elements]
        
        for abqSetName, abqSetValues in dict(abqPart.sets).items():
            # get labels from abaqus database
            nodeLabelList = [n.label for n in abqSetValues.nodes]
            # for each node get index from the list of current nodes
            listOfIndices = [currentNodeLabels.index(lab) for lab in nodeLabelList]
            # from list of indices get list of node objects
            listOfNodes = [nodes[i] for i in listOfIndices]
            nSet['N-' + abqSetName] = listOfNodes

            elementLabelList = [el.label for el in abqSetValues.elements]
            listOfIndices = [currentElLabels.index(lab)
                             for lab in elementLabelList]
            listOfElements = [elements[i] for i in listOfIndices]
            elSet['EL-' + abqSetName] = listOfElements
        
        surfaces = defaultdict(list)
        for abqSurfName, abqSurfValues in dict(abqPart.surfaces).items():
            nodeLabelList = [n.label for n in abqSurfValues.nodes]
            listOfIndices = [currentNodeLabels.index(lab) for lab in nodeLabelList]
            listOfNodes = [nodes[i] for i in listOfIndices]
            listOfUniqueNodes = sorted(list(set(listOfNodes)),
                                          key=lambda n: n.label)
            nSet['S-' + abqSurfName] = listOfUniqueNodes

            elementLabelList = [el.label for el in abqSurfValues.elements]
            listOfIndices = [currentElLabels.index(lab)
                             for lab in elementLabelList]
            listOfElements = [elements[i] for i in listOfIndices]
            listOfUniqueElements = sorted(list(set(listOfElements)),
                                          key=lambda e: e.label)
            elSet['S-' + abqSurfName] = listOfUniqueElements
            
            surfaces[abqSurfName] = {'nodes': nSet['S-' + abqSurfName],
                                     'elements': elSet['S-' + abqSurfName],
                                     'sides': str(abqSurfValues.sides[0])}
        
        return cls(partName=name, partNodes=nodes, partElements=elements,
                   elementSets=elSet, nodeSets=nSet, surfaces=surfaces)

    def __str__(self):
        return pprint.pformat(self.__dict__, width=2)
    
    def __repr__(self):
        return 'PART-%s' % self.name

    def getNodesFromLabelList(self, labelList):
        """Function to retrieve the nodes from list of node labels

        Parameters
        ----------
        labelList: list
            list of integers describing node labes

        Returns
        -------
        list
            list of Node objects
        """
        currentLabels = [n.label for n in self.nodes]
        listOfIndices = [currentLabels.index(lab) for lab in labelList]
        listOfNodes = [self.nodes[i] for i in listOfIndices]
        return listOfNodes

    def getElementsFromLabelList(self, labelList):
        """Function to retreive the elements from list of
        elements labels.

        Parameters
        ----------
        labelList: list
            list of integers referring to element labels

        Returns
        -------
        list
            list of Element objects
        """
        currentLabels = [e.label for e in self.elements]
        listOfIndices = [currentLabels.index(lab) for lab in labelList]
        listOfElements = [self.elements[i] for i in listOfIndices]
        return listOfElements
    
    def getElementsByType(self):
        """Function used to create a dictionary of elements with
        element types used as keys
        
        Returns
        -------
        defaultdict(list)
            dictionary of elements with elementtypes used as keys
        """
        elementByType = defaultdict(list)
        for e in self.elements:
            elementByType[e.type].append(e)
        
        return elementByType
    
    # def getMinMaxLabels(self, nodes=None, elements=None):
    #     if nodes:
    #         labels = [n.label for n in self.nodes]
    #         return (min(labels), max(labels))
    #     elif elements:
    #         labels = [e.label for e in self.elements]
    #         return (min(labels), max(labels))
    
    def renumberNodes(self, new_label_list):
        # rangeOfLabels = xrange(startLabel, len(self.nodes) + startLabel)
        map(lambda node, newLab: node.changeLabel(newLab), self.nodes, new_label_list)
    
    def renumberElements(self, new_label_list):
        # rangeOfLabels = xrange(startLabel, len(self.nodes) + startLabel)
        map(lambda element, newLab: element.changeLabel(newLab), self.elements, new_label_list)
        

    def setElementTypeFormat(self, newFormat):
        """Function to change element types in dictionary
        elementsByType (for example from C3D20R to 116)

        Parameters
        ----------
        newFormat : str
            new format (eg 'UNV')
        """
        # create a temporary dict
        tempElementByType = defaultdict(list)
        # iterate over all element types in the dict
        for elTypeName, elValues in self.elementsByType.items():
            # get new format for each type fo element
            # print elTypeName, elValues
            new_el_type = element_library.convert_to_specific_format(general_format=elTypeName,
                                                                     output=newFormat)
            # newElType = self.getDiffFormatForElType(oldElType=elTypeName,
            #                                         newMeshFormat=newFormat)
            tempElementByType[new_el_type] = elValues
        # swap temporary dict with dict with new formats
        self.elementsByType = tempElementByType
    
    def reorderNodesInElType(self, meshFormat):
        """Function used to reoder nodes. By default the node
        order is the same as in Abaqus.

        Parameters
        ----------
        meshFormat : str
            Format of mesh to be converted to
        """
        # C3D20R
        # abq = [5, 6, 8, 7, 1, 2, 4, 3, 12, 11,
        #        10, 9, 13, 14, 15, 16, 18, 17, 19, 20]
        # unv = [5, 12, 6, 11, 8, 10, 7, 9, 18, 17, 19,
        #        20, 1, 13, 2, 14, 4, 15, 3, 16]
        # C3D10
        # abq = [4, 3, 1, 2, 7, 6, 5, 9, 8, 10]
        # unv = [4, 7, 3, 6, 1, 5, 9, 8, 10, 2]
        # C3D15
        # abq = [3, 2, 1, 6, 5, 4, 9, 8, 7, 10, 11, 12, 14, 13, 15]
        # unv = [3, 9, 2, 8, 1, 7, 14, 13, 15, 6, 10, 5, 11, 4, 12]
        # idx - order to be used in function
        # idx = [abq.index(i) for i in unv]
        def changeOrder(elements, order):
            for el in elements:
                el.connectivity = [el.connectivity[i] for i in order]
        if meshFormat == 'UNV':
            for elType, elements in self.elementsByType.items():
                if '118' == elType:
                    order = [0, 4, 1, 5, 2, 6, 7, 8, 9, 3]
                    changeOrder(elements, order)
                elif '113' == elType:
                    order = [0, 6, 1, 7, 2, 8, 12, 13, 14,
                             3, 9, 4, 10, 5, 11]
                    changeOrder(elements, order)
                elif '116' == elType:
                    order = [0, 8, 1, 9, 2, 10, 3, 11,
                             16, 17, 18, 19, 4, 12, 5,
                             13, 6, 14, 7, 15]
                    changeOrder(elements, order)


    
class Mesh(object):
    """Mesh is the most general class used to import, store
    and export mesh data. The idea is to initialise the constructor,
    then import mesh from db file. Finally, the mesh can be
    exported to an external format. For example
    
    >>> mesh = Mesh()
    >>> mesh.importFromDbFile(pathToDbFile='mesh.db')
    >>> mesh.exportToCalculix(exportedFilename='Calculix.inp')
    >>> mesh.exportToUnvFormat(exportedFilename='Salome.unv')
    
    Attributes
    ----------
    modelName : string
        name of imported model
    parts : list
        list of imported parts
    assemblyMesh: dictionary
        the dictionary contains parts, but those have renumbered\
        node and element labels, so that the labels are not\
        repeating
    """

    def __init__(self, modelName, dictOfParts, asblyElementSets=None,
                 asblyNodeSets=None, asblySurfaces=None):
        self.modelName = modelName
        self.parts = dictOfParts

        # assembly element sets
        if asblyElementSets is None:
            self.elSet = defaultdict(list)
        else:
            self.elSet = asblyElementSets
        # assembly node sets
        if asblyNodeSets is None:
            self.nSet = defaultdict(list)
        else:
            self.nSet = asblyNodeSets
        # assembly surfaces
        if asblySurfaces is None:
            self.surfaces = defaultdict(list)
        else:
            self.surfaces = asblySurfaces

        self.renumberMesh()
        self.ccxElSetSurfDef = defaultdict(list)

    def __str__(self):
        if len(self.__dict__.keys()) == 0:
            return 'Mesh object is empty. Data needs to be loaded first'
        return pprint.pformat(self.__dict__, width=2)

    @classmethod
    def importFromAbaqusCae(cls, abqModelName, abqRootAssembly):
        """Function to initiate the Mesh object

        Parameters
        ----------
        abqModelName : str
            name of the Abaqus model
        abqPartList : list
            list of Abaqus Parts to export mesh from

        Returns
        -------
        Mesh
            object containing model mesh definition
        """
        parts = OrderedDict((p.name, PartMesh.fromAbaqusCae(p))
                            for p in abqRootAssembly.allInstances.values()
                            if p.excludedFromSimulation is False)
        
        # print parts
        n_set = defaultdict(list)
        e_set = defaultdict(list)
        for setName, setValues in abqRootAssembly.sets.items():
            if setValues.nodes:
                temp_dict = defaultdict(list)
                map(lambda n: temp_dict[n.instanceName].append(n.label), setValues.nodes)
                for inst, n_labels in temp_dict.items():
                    n_objects = parts[inst].getNodesFromLabelList(labelList=n_labels)
                    n_set['N-' + setName].extend(n_objects)
            if setValues.elements:
                temp_dict = defaultdict(list)
                map(lambda e: temp_dict[e.instanceName].append(e.label), setValues.elements)
                for inst, e_labels in temp_dict.items():
                    e_objects = parts[inst].getElementsFromLabelList(labelList=e_labels)
                    e_set['EL-' + setName].extend(e_objects)

        # surfaces[abqSurfName] = {'nodes': nSet['S-' + abqSurfName],
        #                             'elements': elSet['S-' + abqSurfName],
        #                             'sides': str(abqSurfValues.sides[0])}
        # if abqRootAssembly.surfaces.keys():
        #     temp_dict = defaultdict(list)
        #     map(lambda x: expression)
        asbly_surfaces = defaultdict(list)
        for surfName, surfValues in abqRootAssembly.surfaces.items():
            asbly_surfaces[surfName] = defaultdict(list)
            temp_dict = defaultdict(list)
            map(lambda n: temp_dict[n.instanceName].append(n.label), surfValues.nodes)
            for inst, n_labels in temp_dict.items():
                n_objects = parts[inst].getNodesFromLabelList(labelList=n_labels)
                asbly_surfaces[surfName]['nodes'].extend(n_objects)
            
            temp_dict = defaultdict(list)
            map(lambda e: temp_dict[e.instanceName].append(e.label), surfValues.elements)
            for inst, e_labels in temp_dict.items():
                e_objects = parts[inst].getElementsFromLabelList(labelList=e_labels)
                asbly_surfaces[surfName]['elements'].extend(e_objects)
            asbly_surfaces[surfName]['sides'] = str(surfValues.sides[0])
            
        return cls(modelName=abqModelName, dictOfParts=parts,
                   asblyElementSets=e_set, asblyNodeSets=n_set,
                   asblySurfaces=asbly_surfaces)

    @classmethod
    def importFromDbFile(cls, pathToDbFile):
        """Function to initiate the Mesh object

        Parameters
        ----------
        pathToDbFile : str
            path to the db file

        Returns
        -------
        Mesh
            object containing model mesh definition
        """
        with open(pathToDbFile, 'rb') as handle:
            mesh = pickle.load(handle)
        
        return cls(modelName=mesh['modelName'],
                   dictOfParts=mesh['partDict'],
                   asblyElementSets=mesh['element_set'],
                   asblyNodeSets=mesh['node_set'],
                   asblySurfaces=mesh['surfaces'])
    
    def saveToDbFile(self, nameOfDbFile):
        """Function to save model data to db file

        Parameters
        ----------
        nameOfDbFile : str
            name of the file that will be used to store data
        """
        dictToSave = {'modelName': self.modelName,
                      'partDict': self.parts,
                      'element_set': self.elSet,
                      'node_set': self.nSet,
                      'surfaces': self.surfaces,
                      }
        
        with open(nameOfDbFile, 'wb') as handle:
            pickle.dump(dictToSave, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
        print('Mesh has been written into {0} file'.format(nameOfDbFile))

    def renumberMesh(self):
        """Function computes mesh at assembly level from list
        of Part objects. The returned dictionary contains
        parts with renumbered nodes and elements

        Returns
        -------
        defaultdict(list)
            dictionary of parts
        """
        # rng = lambda x: xrange(1, x+1)
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
            partName, partValue = part
            partValue.renumberNodes(new_label_list=new_numbering[i][0])
            partValue.renumberElements(new_label_list=new_numbering[i][1])

    def setCalculixSurfDefinition(self, surface_source):
        """Function converts Part.surfaces into format appropriate
        for Calculix.

        Returns:
            dict: dictionary with surface name as keys and dictionary surface
            definition as value
        """
        # The idea below is to iterate over each surface definition and find
        # out what are the surface nodes and compare them with nodes from each
        # element defined in the surface. Once compared it is possible to figure
        # out which face is used in the definition based on index of surf-node 
        # in element-node.
        # print dict(surface_source)
        # surface_source.ccxElSetSurfDef = defaultdict(list)
        
        # for each surface define
        for surfName, surfValue in surface_source.surfaces.items():
            # get node labels from surface definition
            nodeLabels = [n.label for n in surfValue['nodes']]
            # set temporary value
            tempSurfaceDefinition = defaultdict(list)
            # for each element in surface definition
            for e in surfValue['elements']:
                # find list of pairs [(element, surface face),..]
                elementFacesList = e.getCalculixElSurfaces(surfNodesLabels=nodeLabels,
                                                           surfSide=surfValue['sides'])
                # add values to temporary surface dict
                map(lambda face : tempSurfaceDefinition[face].append(e), elementFacesList)
            # for each item in {'el_face': [el-1, el-2,..]}
            for face, elements in tempSurfaceDefinition.items():
                # create name set
                nameOfElset = 'S-' + surfName + '-' + face
                # add element set to surface_source for each face
                surface_source.elSet[nameOfElset] = elements
                # add apprioprate naming to temporary dict
                surface_source.ccxElSetSurfDef[surfName].append((nameOfElset, face))

    def exportToCalculix(self, exportedFilename):
        """Function to export mesh to Calculix format

        Parameters
        ----------
        exportedFilename : str
            name of the file to export mesh (eg 'calculix.inp')
        """
        # get calculix/abaqus element format for each part
        for part in self.parts.values():
            # if any surface definition exists
            if len(part.surfaces.keys()):
                # compute surface definiton made with elements
                self.setCalculixSurfDefinition(surface_source=part)
                # convert surface definition from elements to element sets
            part.setElementTypeFormat(newFormat='CCX')

        self.setCalculixSurfDefinition(surface_source=self)
        # prepare a dict which will be used to render things in template
        renderDict = {'modelName': self.modelName,
                      'parts': self.parts.values(),
                      'assembly_el_sets': self.elSet,
                      'assembly_n_sets': self.nSet,
                      'assembly_ccx_surfaces': self.ccxElSetSurfDef}
        # load jinja template from file
        # https://stackoverflow.com/a/38642558
        templateLoader = jinja2.FileSystemLoader(searchpath=filePath)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("calculix.tmplt")
        # render template with dict
        outputText = template.render(renderDict)
        # remove all empty lines
        outputText = '\n'.join([i for i in outputText.split('\n') if len(i)])
        outputText += '\n'
        # save input deck
        with open(exportedFilename, 'w') as f:
            f.write(outputText)
        print('Mesh exported to {0}'.format(exportedFilename))

    def exportToUnvFormat(self, exportedFilename):
        """Function to export to UNV format

        Parameters
        ----------
        exportedFilename : str
            name of the file to export mesh (eg 'salome.unv')
        """
        # get unv format for each part
        for part in self.parts.values():
            part.setElementTypeFormat(newFormat='UNV')
            part.reorderNodesInElType(meshFormat='UNV')
        # prepare a dict which will be used to render things in template
        renderDict = {'modelName': self.modelName,
                      'parts': self.parts.values(),
                      'assembly_el_sets': self.elSet,
                      'assembly_n_sets': self.nSet,
                      }
        # renderDict = {'parts': self.parts}
        # load jinja template from file
        # https://stackoverflow.com/a/38642558
        templateLoader = jinja2.FileSystemLoader(searchpath=filePath)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("unv.tmplt")
        # render template with dict
        outputText = template.render(renderDict)
        # remove all empty lines
        outputText = '\n'.join([i for i in outputText.split('\n') if len(i)])
        # save input deck
        with open(exportedFilename, 'w') as f:
            f.write(outputText)
        print('Mesh exported to {0}'.format(exportedFilename))

# if __name__ == '__main__':
#     m = Mesh.importFromDbFile(pathToDbFile='Abaqus.db')
#     m.exportToCalculix('calculix.inp')
#     m.exportToUnvFormat('salome.unv')
