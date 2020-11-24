# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

import sys, os
sys.path.insert(0, './CoFEA')

import cofea
# reload(cofea)

# def abq(pName):
#     from textRepr import prettyPrint as pr
#     from abaqus import *
#     from abaqusConstants import *
#     from caeModules import *

#     modelName = 'Model-2-separate'
#     # p = mdb.models[modelName].parts[pName]
#     p = mdb.models['Model-1'].rootAssembly.allInstances['C3D20R-1']
#     model = cofea.Mesh.importFromAbaqusCae(abqModelName=modelName,
#                                      abqInstanceList=[p,])
#     # model.exportToCalculix(exportedFilename='cofea-{0}.inp'.format(pName))
#     # print model
#     model.saveToDbFile(nameOfDbFile='cofea-{0}.db'.format(pName),
#                        exportedFrom='ABQ')
def main(pName):
    # C3D20R
    # abq = [5, 6, 8, 7, 1, 2, 4, 3, 12, 11, 10, 9, 13, 14, 15, 16, 18, 17, 19, 20]
    # unv = [5, 12, 6, 11, 8, 10, 7, 9, 18, 17, 19, 20, 1, 13, 2, 14, 4, 15, 3, 16]
    # C3D10
    # abq = [4, 3, 1, 2, 7, 6, 5, 9, 8, 10]
    # unv = [4, 7, 3, 6, 1, 5, 9, 8, 10, 2]
    # C3D15
    # abq = [3, 2, 1, 6, 5, 4, 9, 8, 7, 10, 11, 12, 14, 13, 15]
    # unv = [3, 9, 2, 8, 1, 7, 14, 13, 15, 6, 10, 5, 11, 4, 12]
    # idx - order to be used in function
    # idx = [abq.index(i) for i in unv]
    # print idx
    # newAbq = [abq[i] for i in idx]
    # print newAbq
    
    # print idx
    # print 'sdas'
    impMesh = cofea.Mesh.importFromDbFile(pathToDbFile='./samples/cofea-{0}.db'.format(pName))
    impMesh.exportToCalculix(exportedFilename='./samples/cofea-{0}.inp'.format(pName))
    impMesh.exportToUnvFormat(exportedFilename='./samples/cofea-{0}.unv'.format(pName))
    # impMesh = cofea.Mesh.importFromDbFile(pathToDbFile='./fork-mesh/{0}.db'.format(pName))
    # for i in impMesh.parts[0].elements:
        # print i.connectivity
    # impMesh.exportToUnvFormat(exportedFilename='./fork-mesh/{0}.unv'.format(pName))
    
if __name__ == '__main__':
    # pName = 'QUAD-WEDGE-1-0'
    pName = 'C3D15'
    # names = ['C3D10', 'C3D15', 'C3D20R', 'C3D4',
    #          'C3D6', 'C3D8R']
    # abq(pName)
    # for pName in names:
    main(pName)