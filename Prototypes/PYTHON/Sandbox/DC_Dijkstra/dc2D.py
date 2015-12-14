__author__ = 'benjamin'

import numpy as np
import numpy.linalg as la
import itertools as it

# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, dims):

    # Cardinal directions
    dirs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]

    # Vertices of quad
    quad_verts = [np.array([0.0, 0.0]),
                  np.array([1.0, 0.0]),
                  np.array([1.0, 1.0]),
                  np.array([0.0, 1.0])] # traverse verts in CCW manner

    # Edges of quad
    quad_edges = [[0,1],[1,2],[2,3],[3,0]] # traverse edges in CCW manner

    # compute intersection point in the middle of a sign changing edge
    def estimate_hermite(data, v0, v1):
        t0 = .5
        x0 = (1. - t0) * v0 + t0 * v1
        return x0

    # create maximum one vertex per cell
    def create_vertices(data, res, dims):
        dc_verts = dict()
        for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
            cell_origin = np.array([float(x), float(y)])

            quad_signs=[]
            quad_sign_keys=[]
            # Get signs for cube
            for v in quad_verts:
                position = (cell_origin + v*res)
                quad_sign_keys.append(tuple(position))

            for vertex_key in quad_sign_keys:
                c = True
                if vertex_key in data:
                    c = data[vertex_key] > 0
                quad_signs.append(c)

            if all(quad_signs) or not any(quad_signs):
                continue

            # Estimate hermite data
            h_data = []
            for e in quad_edges:
                if quad_signs[e[0]] != quad_signs[e[1]]:
                    h_data.append(estimate_hermite(data, cell_origin + quad_verts[e[0]]*res, cell_origin + quad_verts[e[1]]*res))

            counter = 0
            v = np.array([0.0, 0.0])

            for p in h_data:
                v += np.array(p)
                counter += 1

            v /= 1.0 * counter

            # Throw out failed solutions
            if la.norm(v - cell_origin) > 2 * res:
                continue

            # Emit one vertex per every cube that crosses
            vertex_key = tuple(cell_origin + res/2.0 * np.array([1.0,1.0]))
            dc_verts[vertex_key] = v

        return dc_verts

    # connect vertices to vertices in neighbouring cells, if there are any
    def construct_edges(data, res, dims, dc_verts):
        dc_edges = set()
        for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
            # Emit one edge per each edge that crosses
            cell_origin = np.array([float(x), float(y)])
            vertex_key = tuple(cell_origin + res/2.0 * np.array([1.0,1.0]))
            if vertex_key in dc_verts:
                for i in range(2):
                    if tuple(np.array(vertex_key) + res*dirs[i]) in dc_verts:
                        if (data[tuple(cell_origin+res*dirs[i]+res*dirs[int(not i)])] > 0) != (data[tuple(cell_origin+res*dirs[i])] > 0):
                            neighbour_vertex_key = tuple(np.array(vertex_key) + np.array(dirs[i])*res)
                            edge = tuple([vertex_key, neighbour_vertex_key])
                            dc_edges.add(edge)
            else:
                continue

        return dc_edges

    dc_verts = create_vertices(data, res, dims)
    dc_edges = construct_edges(data, res, dims, dc_verts)

    return dc_verts, dc_edges