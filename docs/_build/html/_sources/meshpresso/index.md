# Meshpresso Mesh Converter

The idea behind of Python Meshpresso module is to allow converting models data between different simulation environments. The Meshpresso module is written in a way that allows to either create a mesh from scratch or import it from different source. Here is the example how to prepare a mesh which is then exported to Calculix input deck. It can also be exported to .db file from which it can be imported back.

```python
# example: prepare db file from scratch
# prepare nodes
n1 = meshpresso.Node(nLabel=1, nCoords=(1.0, 0.0, 0.0))
n2 = meshpresso.Node(nLabel=2, nCoords=(0.0, 1.0, 0.0))
n3 = meshpresso.Node(nLabel=3, nCoords=(0.0, 0.0, 1.0))
# put nodes into the list
nodeList = [n1, n2, n3]
# prepare elements
e1 = meshpresso.Element(elType='C3D4', elLabel=1,
               elConnect=(0, 1, 2),
               partAllNodes=nodeList)
# put elements into the list
elementList = [e1, ]
# create part from nodes and elements
part = meshpresso.PartMesh(partName='TestPart',
                  partNodes=nodeList,
                  partElements=elementList)
# put parts into the list
partList = [part, ]
# create a model
model = meshpresso.ExportMesh(modelName='test',
                     listOfParts=partList)
# do some operations with the model
# for example export model to calculix file
model.exportToCalculix(exportedFilename='test.inp')
# or save it to db file
model.saveToDbFile('dbFile.db')
# example: prepare db file from scratch
# prepare nodes
n1 = meshpresso.Node(nLabel=1, nCoords=(1.0, 0.0, 0.0))
n2 = meshpresso.Node(nLabel=2, nCoords=(0.0, 1.0, 0.0))
n3 = meshpresso.Node(nLabel=3, nCoords=(0.0, 0.0, 1.0))
# put nodes into the list
nodeList = [n1, n2, n3]
# prepare elements
e1 = meshpresso.Element(elType='C3D4', elLabel=1,
               elConnect=(0, 1, 2),
               partAllNodes=nodeList)
# put elements into the list
elementList = [e1, ]
# create part from nodes and elements
part = meshpresso.PartMesh(partName='TestPart',
                  partNodes=nodeList,
                  partElements=elementList)
# put parts into the list
partList = [part, ]
# create a model
model = meshpresso.ExportMesh(modelName='test',
                     listOfParts=partList)
# do some operations with the model
# for example export model to calculix file
model.exportToCalculix(exportedFilename='test.inp')
# or save it to db file
model.saveToDbFile('dbFile.db')
```

In order to load the mesh from db file, the following function can be used:
```python
# example: load mesh from db file
m = meshpresso.ExportMesh.importFromDbFile(pathToDbFile='dbFile.db')
m.exportToCalculix(exportedFilename='test.inp')
```

Documentation of module implementation can be found in the link below:

```{toctree}
api
```
