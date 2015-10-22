# from __future__ import division
from operator import pos

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools as it

from ManifoldNode import ManifoldNode
from dcHelpers import update_mesh_2d, generate_vertex_usage_dict

# Cardinal directions
dirs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]

# Vertices of quad
#quad_verts = [np.array([x, y])
#                   for x in np.arange(0.0,2,1.0)
#                   for y in np.arange(0.0,2,1.0)]
quad_verts = [np.array([0.0, 0.0]), np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.array([0.0, 1.0])] # traverse verts in CCW manner

# Edges of quad
#quad_edges = [[0,1],[0,2],[1,3],[2,3]]
quad_edges = [[0,1],[1,2],[2,3],[3,0]] # traverse edges in CCW manner

# Use non-linear root finding to compute intersection point
def estimate_hermite(data, v0, v1):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    #print 'x0='+str(v0)
    #print 'x1='+str(v1)
    return x0


def tworesolution_dual_contour(dataset,resolutions,dims):
    print "DC FINE"
    [dc_verts_fine, dc_edges_fine, dc_verts_pseudo_fine]=dual_contour(dataset,
                                                                      resolutions['fine'],
                                                                      dims,
                                                                      coarse_level = False)
    print "DC COARSE"
    [dc_verts_coarse, dc_edges_coarse,dc_verts_pseudo_coarse]=dual_contour(dataset,
                                                                           resolutions['coarse'],
                                                                           dims,
                                                                           coarse_level = True)

    dc_verts={'fine':dc_verts_fine, 'coarse':dc_verts_coarse}
    dc_edges={'fine':dc_edges_fine, 'coarse':dc_edges_coarse}
    dc_verts_pseudo={'fine':dc_verts_pseudo_fine, 'coarse':dc_verts_pseudo_coarse}

    return dc_verts, dc_edges, dc_verts_pseudo


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, dims, coarse_level):
    # Compute vertices
    dc_verts = []
    vindex = {}
    dc_manifold_verts = []
    manifold_index = {}

    for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
        o = np.array([float(x), float(y)])

        quad_signs=[]
        quad_sign_keys=[]
        # Get signs for cube
        for v in quad_verts:
            position = (o + v*res)
            quad_sign_keys.append(tuple(position))

        for key in quad_sign_keys:
            c = True
            if key in data:
                c = data[key] > 0
            quad_signs.append(c)

        #print "voxel at "+str(o)+": "+str(quad_signs)

        if all(quad_signs) or not any(quad_signs):
            continue

        #this checks for certain problematic cases and introduces manifold nodes, if necessary
        if coarse_level:
            if quad_signs == [False, True, False, True] or quad_signs == [True, False, True, False]:
                #print quad_signs
                key = tuple(o)
                manifold_index[key] = len(dc_manifold_verts)
                dc_manifold_verts.append(ManifoldNode(o, quad_sign_keys, data, res))

        # Estimate hermite data
        h_data = []
        for e in quad_edges:
            if quad_signs[e[0]] != quad_signs[e[1]]:
                h_data.append(estimate_hermite(data, o + quad_verts[e[0]]*res, o + quad_verts[e[1]]*res))

        counter = 0
        v = np.array([0.0, 0.0])

        for p in h_data:
            v += np.array(p)
            counter += 1

        v /= 1.0 * counter

        # Throw out failed solutions
        if la.norm(v - o) > 2 * res:
            continue

        # Emit one vertex per every cube that crosses
        key = tuple(o)
        vindex[key] = len(dc_verts)
        dc_verts.append(v)

    # Construct faces
    dc_edges = []
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
        # Emit one edge per each edge that crosses
        if (x, y) in vindex:
            o = np.array([float(x), float(y)])
            for i in range(2):
                if tuple(o + res*dirs[i]) in vindex:
                    if (data[tuple(o+res*dirs[i]+res*dirs[int(not i)])] > 0) != (data[tuple(o+res*dirs[i])] > 0):
                        dc_edges.append([vindex[tuple(o)], vindex[tuple(o + np.array(dirs[i])*res)]])
        else:
            continue

    if coarse_level:
        vertex_usage_dict = generate_vertex_usage_dict(dc_edges)

        new_edges_list = []
        new_nodes_list = []
        delete_edges_list = []

        o_idx_nodes =  dc_verts.__len__()
        for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
            # Emit one edge per each edge that crosses
            if (x, y) in manifold_index:
                i = manifold_index[(x, y)]
                global_idx = vindex[(x, y)]

                [new_edges, new_nodes, delete_edges] = dc_manifold_verts[i].resolve(o_idx_nodes,
                                                                                    global_idx,
                                                                                    vindex,
                                                                                    vertex_usage_dict)
                new_edges_list += new_edges
                new_nodes_list += new_nodes
                delete_edges_list += delete_edges
                o_idx_nodes += new_nodes.__len__()

        [dc_verts, dc_edges] = update_mesh_2d(dc_verts, dc_edges, new_edges_list, new_nodes_list, delete_edges_list)

    return np.array(dc_verts), np.array(dc_edges), np.array(dc_manifold_verts)