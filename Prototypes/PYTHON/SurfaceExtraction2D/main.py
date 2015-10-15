__author__ = 'benjamin'

from dc2D import tworesolution_dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from edge import Edge

import numpy as np


def find_closest_edges(_point, _edgelist, _n_closest):
    d_sq_list = [None] * _edgelist.__len__() # empty list for distances point to all quads
    for i in range(_edgelist.__len__()): # iterate over all quads
        d_sq = _edgelist[i].measure_centroid_distance_squared(_point) # distance to centroid
        d_sq_list[i] = d_sq

    idx_list = sorted(range(len(d_sq_list)), key=lambda k: d_sq_list[k])
    n_closest_idx = idx_list[:_n_closest]

    return n_closest_idx


dimensions = {'xmin': 0.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0}
res_fine = 1.0/16.0
res_coarse = res_fine * 8.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

fine_data = sample_data(doubletorus_f, resolutions['fine'], dimensions)
[verts_out_dc, edges_out_dc, verts_pseudo_out_dc] = tworesolution_dual_contour(fine_data, resolutions, dimensions)

N_edges = {'coarse': edges_out_dc['coarse'].shape[0], 'fine': edges_out_dc['fine'].shape[0]}
N_verts = {'coarse': verts_out_dc['coarse'].shape[0], 'fine': verts_out_dc['fine'].shape[0]}

edges = {'coarse': [None] * N_edges['coarse'], 'fine': [None] * N_edges['fine']}
verts = {'coarse': verts_out_dc['coarse'], 'fine': verts_out_dc['fine']} # todo substitute with vertex objects

for i in range(N_edges['coarse']):
    edges['coarse'][i]=Edge(i,edges_out_dc['coarse'],verts_out_dc['coarse'])

import matplotlib.pyplot as plt

fig = plt.figure()

for q in edges_out_dc['fine']:
    vtx = verts_out_dc['fine'][q]
    x = vtx[:,0]
    y = vtx[:,1]
    #plt.plot(x, y, 'b')
    #plt.plot(x, y, 'bo')

for q in edges_out_dc['coarse']:
    vtx = verts_out_dc['coarse'][q]
    x = vtx[:,0]
    y = vtx[:,1]
    plt.plot(x, y, 'k')
    plt.plot(x, y,'ko')

for v in verts_pseudo_out_dc['coarse']:
    x = v.x
    y = v.y
    plt.plot(x, y,'kx')

print verts_pseudo_out_dc

# show voxel data on resolution depending on res_key
res_key = 'coarse'
for key in fine_data:
    if (key[0] % resolutions[res_key] == 0) and (key[1] % resolutions[res_key] == 0):
        if fine_data[key] > 0: # outer point
            plt.plot(key[0],key[1],'b.')
        elif fine_data[key] < 0: # inner point
            plt.plot(key[0],key[1],'r.')

N_closest_candidates = 6 # compute list of N_closest_candidates closest quads
for vertex in verts['fine']:
    closest_idx_candidates = find_closest_edges(vertex, edges['coarse'], N_closest_candidates) # find N closest quads with fast criterion: distance to centroid

    distance_min = np.inf
    for candidate_idx in closest_idx_candidates: # iterate over all candidates from coarse criterion
        projected_point, distance, t = \
            edges['coarse'][candidate_idx].projection_onto_edge(vertex) # find closest quad with fine criterion: projection onto quad

        if abs(distance) < distance_min:
            projected_point_min = projected_point
            distance_min = abs(distance)

    #only plotting information
    start = projected_point_min
    end = vertex
    #plt.plot([start[0],end[0]],[start[1],end[1]],'k',linewidth=2.0)


plt.xlim(xmin = -1, xmax = 7)
plt.ylim(ymin = 1 , ymax = 7)
plt.show()

