from dc3D import tworesolution_dual_contour
import numpy as np
import cPickle


def transform_dict(cellsDict):
    dataset = {}
    for key in cellsDict:
        dataset[key] = -1

    return dataset


wfFile = open('Cantilever/Cells_01', 'rb')
cellsDict = cPickle.load(wfFile)
wfFile.close()

wfFile = open('Cantilever/Dimensions_01', 'rb')
dimensions = cPickle.load(wfFile)
wfFile.close()

res_fine = 1
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

data = transform_dict(cellsDict)

[Fine, Coarse] = tworesolution_dual_contour(data, resolutions, dimensions)

Fine.export_as_stl(filename = 'canfi_fine.stl')
Coarse.export_as_stl(filename = 'canti.stl')
Coarse.export_as_csv('Coarse')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')


for q in Coarse.quads:
    vtx = Coarse.verts[q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

for q in Fine.quads:
    vtx = Fine.verts[q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
#    ax.add_collection3d(poly)


ax.set_xlim3d(dimensions['xmin'], dimensions['xmax'])
ax.set_ylim3d(dimensions['ymin'], dimensions['ymax'])
ax.set_zlim3d(dimensions['zmin'], dimensions['zmax'])
plt.show()


