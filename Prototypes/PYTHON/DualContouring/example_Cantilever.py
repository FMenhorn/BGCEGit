from dc3D import tworesolution_dual_contour

import numpy as np
import dcHelpers

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

[verts_out_dc, quads_out_dc] = tworesolution_dual_contour(data, resolutions, dimensions)

dcHelpers.export_as_stl(quads_out_dc, verts_out_dc, plot_scale = 'coarse', filename = 'canti.stl')

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
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

''' # useful for debugging
for m_e_key, m_edge in manifold_edges_dc[plot_scale].items():
    vtx = verts_out_dc[plot_scale][[m_e_key[0],m_e_key[1]]]
    x = vtx[:, 0]
    y = vtx[:, 1]
    z = vtx[:, 2]
    vtx = [zip(x,y,z)]
    line = Line3DCollection(vtx,color='r',linewidth=1.0)
    ax.add_collection3d(line)

    for local_idx in range(2):
        if m_edge.v_kind[local_idx] == "inside":
            plotcolor = 'ro'
        elif m_edge.v_kind[local_idx] == "outside":
            plotcolor = 'gx'
        elif m_edge.v_kind[local_idx] == "manifold":
            plotcolor = 'k*'
        elif m_edge.v_kind[local_idx] == "hybrid":
            plotcolor = 'ks'
        else:
            print "ERROR!"
        vtx = verts_out_dc[plot_scale][m_e_key[local_idx]]
        ax.plot([vtx[0]],[vtx[1]],[vtx[2]],plotcolor)
'''

plot_scale = 'fine'
for q in quads_out_dc[plot_scale]:
    vtx = verts_out_dc[plot_scale][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)
'''
print "number of faces: "+str(quads_out_dc[plot_scale].__len__())
print "number of tri: "+str(no_t)
print "number of quads: "+str(no_q)
print "number of pents: "+str(no_p)
print "number of hex: "+str(no_h)
print "number of unex:"+str(no_u)
'''
ax.set_xlim3d(dimensions['xmin'], dimensions['xmax'])
ax.set_ylim3d(dimensions['ymin'], dimensions['ymax'])
ax.set_zlim3d(dimensions['zmin'], dimensions['zmax'])
plt.show()


