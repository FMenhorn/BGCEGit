

__author__ = 'benjamin + JC'

import dc3D_real

from edge import Edge

from vertX import VerteX

import numpy as np

import cPickle

wfFile = open('Cells', 'rb')
cellsDict= cPickle.load(wfFile)
wfFile.close()

wfFile = open('Dimensions', 'rb')
dimensions= cPickle.load(wfFile)
wfFile.close()


def find_closest_quads(_point, _quadlist, _n_closest):
    d_sq_list = [None] * _quadlist.__len__()
    for i in range(_quadlist.__len__()):
        d_sq = _quadlist[i].measure_centroid_distance_squared(_point)
        d_sq_list[i] = d_sq

    idx_list = sorted(range(len(d_sq_list)), key=lambda k: d_sq_list[k])
    n_closest_idx = idx_list[:_n_closest]

    return n_closest_idx


res_fine = 1
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}


[verts_out_dc, quads_out_dc] = dc3D_real.tworesolution_dual_contour(cellsDict, resolutions, dimensions)


quads = {'coarse': [None] * quads_out_dc['coarse'].shape[0], 'fine': []}
verts = {'coarse': verts_out_dc['coarse'], 'fine': verts_out_dc['fine']}

for i in range(quads['coarse'].__len__()):
    quads['coarse'][i]=Edge(i,quads_out_dc['coarse'],verts_out_dc['coarse'])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

plane_oo = [False] * quads['coarse'].__len__()
for q in quads['coarse']:
    vtx = q.vertices_plane
    M = vtx[1:4,:]-vtx[0,:]
    plane_oo[q.quad_id] = abs(np.linalg.det(M))<10**-10
    vtx_orig = verts['coarse'][q.vertex_ids]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    x_orig = vtx_orig[:,0].tolist()
    y_orig = vtx_orig[:,1].tolist()
    z_orig = vtx_orig[:,2].tolist()
    vtx = [zip(x,y,z)]
    vtx_orig = [zip(x_orig,y_orig,z_orig)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

for q in quads_out_dc['fine']:
    vtx = verts['fine'][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

for vertex in verts['fine']:
    closest_idx = find_closest_quads(vertex, quads['coarse'], 6)
    d_min = np.inf

    for idx in closest_idx:
        start, d, u, v = quads['coarse'][idx].projection_onto_edge(vertex)
        if abs(d) < d_min:
            start_min = start
            d_min = abs(d)

    start = start_min
    end = vertex
    ax.plot([start[0],end[0]],[start[1],end[1]],[start[2],end[2]],'k',linewidth=2.0)
    ax.plot([end[0]],[end[1]],[end[2]],'o')

ax.set_xlim3d(dimensions['xmin']-5,dimensions['xmax']+5 )
ax.set_ylim3d(dimensions['ymin']-5,dimensions['ymax']+5)
ax.set_zlim3d(dimensions['zmin']-5,dimensions['zmax']+5)
plt.show()

print "finish"


