__author__ = 'benjamin'

from dc3D import tworesolution_dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from quad import Quad

import numpy as np


def find_closest_quads(_point, _quadlist, _n_closest):
    d_sq_list = [None] * _quadlist.__len__() # empty list for distances point to all quads
    for i in range(_quadlist.__len__()): # iterate over all quads
        d_sq = _quadlist[i].measure_centroid_distance_squared(_point) # distance to centroid
        d_sq_list[i] = d_sq

    idx_list = sorted(range(len(d_sq_list)), key=lambda k: d_sq_list[k])
    n_closest_idx = idx_list[:_n_closest]

    return n_closest_idx


dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
res_fine = 1
res_coarse = res_fine * 4.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

fine_data = sample_data(sphere_f, resolutions['fine'], dimensions)
[verts_out_dc, quads_out_dc] = tworesolution_dual_contour(fine_data, resolutions, dimensions)

N_quads = {'coarse': quads_out_dc['coarse'].shape[0], 'fine': quads_out_dc['fine'].shape[0]}
N_verts = {'coarse': verts_out_dc['coarse'].shape[0], 'fine': verts_out_dc['fine'].shape[0]}

quads = {'coarse': [None] * N_quads['coarse'], 'fine': [None] * N_quads['fine']}
verts = {'coarse': verts_out_dc['coarse'], 'fine': verts_out_dc['fine']} # todo substitute with vertex objects

for i in range(N_quads['coarse']):
    quads['coarse'][i]=Quad(i,quads_out_dc['coarse'],verts_out_dc['coarse'])

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
    #poly.set_alpha(.25)
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

# do projection of fine verts on coarse quads
N_closest_candidates = 6 # compute list of N_closest_candidates closest quads
for vertex in verts['fine']:
    closest_idx_candidates = find_closest_quads(vertex, quads['coarse'], N_closest_candidates) # find N closest quads with fast criterion: distance to centroid

    distance_min = np.inf
    for candidate_idx in closest_idx_candidates: # iterate over all candidates from coarse criterion
        projected_point, distance, u, v = \
            quads['coarse'][candidate_idx].projection_onto_quad(vertex) # find closest quad with fine criterion: projection onto quad

        if abs(distance) < distance_min:
            projected_point_min = projected_point
            distance_min = abs(distance)

    #only plotting information
    start = projected_point_min
    end = vertex
    ax.plot([start[0],end[0]],[start[1],end[1]],[start[2],end[2]],'k',linewidth=2.0)

ax.set_xlim3d(2, 6)
ax.set_ylim3d(2, 6)
ax.set_zlim3d(2, 6)
plt.show()


