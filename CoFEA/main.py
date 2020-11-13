"""
:noindex:
"""
import cofea
import os 
filePath = os.path.dirname(os.path.realpath(__file__))

def main():
    # example: prepare db file from scratch
    # prepare nodes
    n1 = cofea.Node(nLabel=1, nCoords=(1.0, 0.0, 0.0))
    n2 = cofea.Node(nLabel=2, nCoords=(0.0, 1.0, 0.0))
    n3 = cofea.Node(nLabel=3, nCoords=(0.0, 0.0, 1.0))
    # put nodes into the list
    nodeList = [n1, n2, n3]
    # prepare elements
    e1 = cofea.Element(elType='C3D4', elLabel=1,
                       elConnect=(0, 1, 2),
                       partAllNodes=nodeList)
    # put elements into the list
    elementList = [e1, ]
    # create part from nodes and elements
    part = cofea.PartMesh(partName='TestPart',
                          partNodes=nodeList,
                          partElements=elementList)
    # put parts into the list
    partList = [part, ]
    # create a model
    model = cofea.ExportMesh(modelName='test',
                             listOfParts=partList)
    # do some operations with the model
    # for example export model to calculix file
    model.exportToCalculix(exportedFilename='test.inp')
    # or save it to db file
    model.saveToDbFile('dbFile.db')
    
    # example: load mesh from db file
    m = cofea.ExportMesh.importFromDbFile(pathToDbFile='dbFile.db')
    m.exportToCalculix(exportedFilename='ccx.inp')
    m.exportToUnvFormat(exportedFilename='salome.unv')

if __name__ == '__main__':
    main()
