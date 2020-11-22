import os
import cofea

dirPath = os.path.dirname(os.path.realpath(__file__))
directory = dirPath + '/samples/'

def test_convertToInp():
    for filename in os.listdir(directory):
        if filename.endswith(".db"): 
            dbFile = os.path.join(directory, filename)
            impMesh = cofea.Mesh.importFromDbFile(pathToDbFile=dbFile)
            impMesh.exportToCalculix(exportedFilename=dbFile.replace('.db',
                                                                     '.inp'))
def test_convertToUnv():
    directory = dirPath + '/samples/'
    for filename in os.listdir(directory):
        if filename.endswith(".db"): 
            dbFile = os.path.join(directory, filename)
            impMesh = cofea.Mesh.importFromDbFile(pathToDbFile=dbFile)
            impMesh.exportToUnvFormat(exportedFilename=dbFile.replace('.db',
                                                                      '.unv'))

def test_simpleMeshCreation():
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
    model = cofea.Mesh(modelName='test',
                       listOfParts=partList)
    # save it to db file
    model.saveToDbFile(directory + 'simple.db')
    
    # example: load mesh from db file
    m = cofea.Mesh.importFromDbFile(pathToDbFile=directory + 'simple.db')
    m.exportToCalculix(exportedFilename=directory + 'simple-ccx.inp')
    m.exportToUnvFormat(exportedFilename=directory + 'simple-salome.unv')
    
if __name__ == '__main__':
    test_convertToInp()
    test_convertToUnv()
    test_simpleMeshCreation()