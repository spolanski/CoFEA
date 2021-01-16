# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Slawomir Polanski

"""
from collections import defaultdict, OrderedDict
import pickle
import pprint
import jinja2

import os
filePath = os.path.dirname(os.path.realpath(__file__))

def _getChunks(itemsToChunk, numOfChunks):
    """Useful function to create lists of lists from list

    Parameters
    ----------
    itemsToChunk : list
        list of objects
    numOfChunks : int
        length of internal list

    Returns
    -------
    list
        list of lists
    """
    temp = [itemsToChunk[i:i + numOfChunks]
            for i in xrange(0, len(itemsToChunk), numOfChunks)]
    return temp
            
class Node(object):
    """Used to create node objects from external data

    Attributes
    ----------
    label: int
        Node number
    coordinates: tuple
        Node coordinates
    """

    def __init__(self, nLabel, nCoords):
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

    def __repr__(self):

        return 'ND-%d' % self.label

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
        self.type = str(elType)
        self.label = elLabel
        self.connectivity = [partAllNodes[c] for c in elConnect]

    def __repr__(self):
        
        return 'EL-%d' % self.label
    
    def getNodeLabels(self):
        """Function returns labels of nodes which building the element

        Returns
        -------
        list
            list of integers describing node labels
        """
        return [n.label for n in self.connectivity]

        
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
    """
    # UNV element types
    # http://victorsndvg.github.io/FEconv/formats/unv.xhtml
    __elementTypes = (
        OrderedDict([('ABQ', 'S3'), ('CCX', 'S3'), ('UNV', '91')]),
        OrderedDict([('ABQ', 'STRI65'), ('CCX', 'S6'), ('UNV', '92')]),
        OrderedDict([('ABQ', 'S4'), ('CCX', 'S4'), ('UNV', '94')]),
        OrderedDict([('ABQ', 'S4R'), ('CCX', 'S4R'), ('UNV', '94')]),
        OrderedDict([('ABQ', 'C3D4'), ('CCX', 'C3D4'), ('UNV', '111')]),
        OrderedDict([('ABQ', 'C3D6'), ('CCX', 'C3D6'), ('UNV', '112')]),
        OrderedDict([('ABQ', 'C3D8'), ('CCX', 'C3D8'), ('UNV', '115')]),
        OrderedDict([('ABQ', 'C3D8R'), ('CCX', 'C3D8R'), ('UNV', '115')]),
        OrderedDict([('ABQ', 'C3D10'), ('CCX', 'C3D10'), ('UNV', '118')]),
        OrderedDict([('ABQ', 'C3D15'), ('CCX', 'C3D15'), ('UNV', '113')]),
        OrderedDict([('ABQ', 'C3D20R'), ('CCX', 'C3D20R'), ('UNV', '116')]),
    )
    
    def __init__(self, partName, partNodes, partElements,
                 elementSets=None, nodeSets=None):
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

    def __str__(self):
        return pprint.pformat(self.__dict__, width=2)
    
    def __repr__(self):
        return 'PART-%s' % self.name

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

        for setName, setValues in dict(abqPart.sets).items():
            nodeLabelList = [n.label for n in setValues.nodes]
            currentLabels = [n.label for n in nodes]
            listOfIndices = [currentLabels.index(lab) for lab in nodeLabelList]
            listOfNodes = [nodes[i] for i in listOfIndices]
            nSet['N_' + setName] = listOfNodes

            elementLabelList = [el.label for el in setValues.elements]
            currentLabels = [e.label for e in elements]
            listOfIndices = [currentLabels.index(lab)
                             for lab in elementLabelList]
            listOfElements = [elements[i] for i in listOfIndices]
            elSet['EL_' + setName] = listOfElements
        
        return cls(partName=name, partNodes=nodes, partElements=elements,
                   elementSets=elSet, nodeSets=nSet)

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

    def getDiffFormatForElType(self, oldElType, newMeshFormat):
        """Function to retrieve name of element type for a
        specific software

        Parameters
        ----------
        oldElType : str
            name of the element type that needs to be
            converted (eg 'C3D8R')
        newMeshFormat : str
            new mesh format (eg 'UNV')

        Returns
        -------
        str
            name of the element type in new format

        Raises
        ------
        ValueError
            error appears when the specific element type
            is not implemented
        """
        newElType = False
        for elTypes in self.__elementTypes:
            if oldElType in elTypes.values():
                newElType = elTypes[newMeshFormat]
        if newElType is False:
            er = "Element type {0} in not implemented yet".format(oldElType)
            raise ValueError(er)
        
        return newElType

    def setElementTypeFormat(self, newFormat):
        """Function to change element types in dictionary
        elementsByType (for example from C3D20R to )

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
            newElType = self.getDiffFormatForElType(oldElType=elTypeName,
                                                    newMeshFormat=newFormat)
            tempElementByType[newElType] = elValues
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

    def __init__(self, modelName, listOfParts):
        self.modelName = modelName
        self.parts = listOfParts
        # TODO computeAssemblyMesh function needs to be finished
        self.assemblyMesh = self.computeAssemblyMesh()

    def __str__(self):
        if len(self.__dict__.keys()) == 0:
            return 'Mesh object is empty. Data needs to be loaded first'
        return pprint.pformat(self.__dict__, width=2)

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
    
    @classmethod
    def importFromAbaqusCae(cls, abqModelName, abqPartList):
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
        parts = [PartMesh.fromAbaqusCae(p) for p in abqPartList]
        return cls(modelName=abqModelName, listOfParts=parts)

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
                   listOfParts=mesh['partList'])
    
    def saveToDbFile(self, nameOfDbFile):
        """Function to save model data to db file

        Parameters
        ----------
        nameOfDbFile : str
            name of the file that will be used to store data
        """
        dictToSave = {'modelName': self.modelName,
                      'partList': self.parts
                      }
        
        with open(nameOfDbFile, 'wb') as handle:
            pickle.dump(dictToSave, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
        print('Mesh has been written into {0} file'.format(nameOfDbFile))

    def computeAssemblyMesh(self):
        """Function computes mesh at assembly level from list
        of Part objects. The returned dictionary contains
        parts with renumbered nodes and elements

        Returns
        -------
        defaultdict(list)
            dictionary of parts
        """
        
        # TODO: Function is not finished
        assembly = defaultdict(list)
        for part in self.parts:
            assembly[part.name] = part
        
        return assembly

    def exportToCalculix(self, exportedFilename):
        """Function to export mesh to Calculix format

        Parameters
        ----------
        exportedFilename : str
            name of the file to export mesh (eg 'calculix.inp')
        """
        # get calculix/abaqus element format for each part
        for p in self.parts:
            p.setElementTypeFormat(newFormat='CCX')
            # p.reorderNodesInElType()
        # prepare a dict which will be used to render things in template
        renderDict = {'modelName': self.modelName,
                      'parts': self.parts}
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
        for p in self.parts:
            p.setElementTypeFormat(newFormat='UNV')
            p.reorderNodesInElType(meshFormat='UNV')
        # prepare a dict which will be used to render things in template
        renderDict = {
            'parts': self.parts,
            'coord_sys': self.coordinate_system
            }
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
