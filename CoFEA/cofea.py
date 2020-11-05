# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Slawomir Polanski

"""
from collections import defaultdict
import pickle
import pprint


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
    theirs type, label, and connection to nodes
    
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

    @classmethod
    def fromAbaqus(cls, abqPart):
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

        for setName, setValues in dict(abqPart.sets).iteritems():
            nodeLabelList = [n.label for n in setValues.nodes]
            currentLabels = [n.label for n in nodes]
            listOfIndices = [currentLabels.index(lab) for lab in nodeLabelList]
            listOfNodes = [nodes[i] for i in listOfIndices]
            nSet['N_' + setName] = listOfNodes

            elementLabelList = [el.label for el in setValues.elements]
            currentLabels = [e.label for e in elements]
            listOfIndices = [currentLabels.index(lab) for lab in elementLabelList]
            listOfElements = [elements[i] for i in listOfIndices]
            elSet['EL_' + setName] = listOfElements
        
        return cls(partName=name, partNodes=nodes, partElements=elements,
                   elementSets=elSet, nodeSets=nSet)
        
    def __str__(self):
        return pprint.pformat(self.__dict__, width=2)
    
    def __repr__(self):
        return 'PART-%s' % self.namez
            
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
    

class ExportMesh(object):
    """Mesh is the most general class used to import, store\
    and export mesh data. The idea is to initialise the constructor,\
    then import mesh from db file. Finally, the mesh can be\
    exported to an external format. For example
    
    >>> mesh = Mesh()
    >>> mesh.importFromDbFile(pathToDbFile='mesh.db')
    >>> mesh.exportToCalculix(exportedFilename='Calculix.inp')
    
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
        # computeAssemblyMesh function needs to be finished
        self.assemblyMesh = self.computeAssemblyMesh()

    @classmethod
    def importFromAbaqus(cls, abqModelName, abqPartList):
        """Function to initiate the ExportMesh object

        Parameters
        ----------
        abqModelName : str
            name of the Abaqus model
        abqPartList : list
            list of Abaqus Parts to export mesh from

        Returns
        -------
        ExportMesh
            object containing model mesh definition
        """
        parts = [PartMesh.fromAbaqus(p) for p in abqPartList]
        return cls(modelName=abqModelName, listOfParts=parts)

    @classmethod
    def importFromDbFile(cls, pathToDbFile):
        """Function to initiate the ExportMesh object

        Parameters
        ----------
        pathToDbFile : str
            path to the db file

        Returns
        -------
        ExportMesh
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
                      'partList': self.parts}
        
        with open(nameOfDbFile, 'wb') as handle:
            pickle.dump(dictToSave, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
        print 'Mesh has been written into {0} file'.format(nameOfDbFile)
            
    def __str__(self):
        if len(self.__dict__.keys()) == 0:
            return 'Mesh object is empty. Data needs to be loaded first'
        
        return pprint.pformat(self.__dict__, width=2)

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
        """Function used to generate input deck for Calculix software

        Parameters
        ----------
        exportedFilename: str
            name of the file to be created
        """
        deck = '*HEADING\nModel name: {0}\n'.format(self.modelName)
        
        def getChunkStrFromList(itemList, itemsInChunk=10, tab=True):
            partOfDeck = ''
            if len(itemList) <= itemsInChunk:
                temp = len(itemList) * '{:>6},'
                partOfDeck += temp.format(*elInput)
                partOfDeck += '\n'
            else:
                # Split into chunks
                # https://stackoverflow.com/a/312464
                chunks = [itemList[i:i + itemsInChunk]
                          for i in xrange(0, len(itemList), itemsInChunk)]
                
                temp = len(chunks[0]) * '{:>6},'
                partOfDeck = temp.format(*chunks[0])
                partOfDeck += '\n'
                
                if tab is True:
                    tabCharacter = '\t'
                else:
                    tabCharacter = ''
                    
                for ch in chunks[1:]:
                    temp = tabCharacter + len(ch) * '{:>6},' + '\n'
                    partOfDeck += temp.format(*ch)
            
            return partOfDeck

        for partName, partObject in self.assemblyMesh.iteritems():
            deck += '*NODE, NSET={0}-NALL\n'.format(partName)
            # https://stackoverflow.com/a/8234511
            # TODO: assembly mesh not part
            for node in partObject.nodes:
                nInput = (node.label, node.coordinates[0],
                          node.coordinates[1], node.coordinates[2])
                deck += '{:>8}, {:>12.6},{:>12.6},{:>12.6}\n'.format(*nInput)
            # prepare elements to write them into input deck
            for elType, elementList in partObject.elementsByType.iteritems():
                deck += '*ELEMENT, TYPE={0}, ELSET={1}-ALL\n'.format(elType,
                                                                     partName)
                for element in elementList:
                    connectivityIndices = element.getNodeLabels()
                    elInput = [element.label]
                    elInput.extend(connectivityIndices)
                    # I have implemented 10 entries max in if-else
                    # statement and getChunkStrFromList() function
                    chunkedDeck = getChunkStrFromList(itemList=elInput,
                                                      itemsInChunk=10,
                                                      tab=True)
                    deck += chunkedDeck
            if len(partObject.nSet.keys()):
                # prepare node sets to write to input deck
                for nSetName, nodeSetValue in partObject.nSet.iteritems():
                    deck += '*NSET, NSET={0}-{1}\n'.format(partName, nSetName)
                    nodeSetLabels = [n.label for n in nodeSetValue]
                    chunkedDeck = getChunkStrFromList(itemList=nodeSetLabels,
                                                      itemsInChunk=10,
                                                      tab=False)
                    deck += chunkedDeck
            if len(partObject.elSet.keys()):
                # prepare element sets to write to input deck
                for elSetName, elSetValue in partObject.elSet.iteritems():
                    deck += '*ELSET, ELSET={0}-{1}\n'.format(partName,
                                                             elSetName)
                    elSetLabels = [e.label for e in elSetValue]
                    chunkedDeck = getChunkStrFromList(itemList=elSetLabels,
                                                      itemsInChunk=10,
                                                      tab=False)
                    
                    deck += chunkedDeck
        # write Calculix input deck
        with open('{0}'.format(exportedFilename), 'w') as f:
            f.write(deck)
        print 'Calculix deck was written into {0}'.format(exportedFilename)
