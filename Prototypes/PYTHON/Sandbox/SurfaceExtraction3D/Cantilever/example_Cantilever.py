from dc3D_real import tworesolution_dual_contour


import numpy as np

import cPickle

wfFile = open('Cells', 'rb')
cellsDict= cPickle.load(wfFile)
wfFile.close()

wfFile = open('Dimensions', 'rb')
dimensions= cPickle.load(wfFile)
wfFile.close()
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

for cell in cellsDict:
    x = cell[0] + .5
    y = cell[1] + .5
    z = cell[2] + .5
    ax.plot([x],[y],[z],'.b')

ax.set_xlim3d(dimensions['xmin'], dimensions['xmax'])
ax.set_ylim3d(dimensions['ymin'], dimensions['ymax'])
ax.set_zlim3d(dimensions['zmin'], dimensions['zmax'])
plt.show()

quit()
'''
res_fine = 1
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}


[verts_out_dc, quads_out_dc, manifold_edges_dc] = tworesolution_dual_contour(cellsDict, resolutions, dimensions)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

plot_scale = 'coarse'
for q in quads_out_dc[plot_scale]:
    vtx = verts_out_dc[plot_scale][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(1)
    ax.add_collection3d(poly)

for m_e in manifold_edges_dc[plot_scale]:
    vtx = verts_out_dc[plot_scale][[m_e[0],m_e[1]]]
    x = vtx[:, 0]
    y = vtx[:, 1]
    z = vtx[:, 2]
    vtx = [zip(x,y,z)]
    line = Line3DCollection(vtx,color='r',linewidth=10.0)
    ax.add_collection3d(line)

ax.set_xlim3d(dimensions['xmin'], dimensions['xmax'])
ax.set_ylim3d(dimensions['ymin'], dimensions['ymax'])
ax.set_zlim3d(dimensions['zmin'], dimensions['zmax'])
plt.show()


