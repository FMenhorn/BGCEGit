import numpy as np
import numpy.linalg as la
import itertools as it

from ManifoldNode import ManifoldNode
from dcHelpers import resolve_manifold_nodes, is_inside

# Cardinal directions
dirs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]

# Vertices of quad
quad_verts = [np.array([0.0, 0.0]),
              np.array([1.0, 0.0]),
              np.array([1.0, 1.0]),
              np.array([0.0, 1.0])] # traverse verts in CCW manner

# Edges of quad
quad_edges = [[0,1],[1,2],[2,3],[3,0]] # traverse edges in CCW manner


def estimate_hermite(data, gdata, v0, v1, res, res_fine, coarse_level):
    data_v0 = is_inside(data, tuple(v0))
    data_v1 = is_inside(data, tuple(v1))

    if coarse_level:
        res_min = res_fine
    else:
        res_min = res

    x0 = .5*(v0 + v1)
    while res != res_min:
        data_x0 = is_inside(data, tuple(x0))
        if data_v0 != data_x0:
            v1 = x0
        elif data_v1 != data_x0:
            v0 = x0
        else:
            print "ERROR!"
            quit()
        x0 = .5*(v0 + v1)
        res /= 2.0

    dfdx = (np.array(gdata[tuple(v0)]) + np.array(gdata[tuple(v1)]))
    dfdx = dfdx / np.linalg.norm(dfdx)

    #print str(dfdx) + "@" + str(x0) + "\t FROM:"+str(gdata[tuple(v0)])+ " and "+str(gdata[tuple(v1)])

    return x0, dfdx


def tworesolution_dual_contour(dataset, gdata, resolutions,dims):
    [dc_verts_fine, dc_edges_fine]=dual_contour(dataset,
                                                gdata,
                                                resolutions['fine'],
                                                resolutions['fine'],
                                                dims,
                                                coarse_level = False)

    [dc_verts_coarse, dc_edges_coarse]=dual_contour(dataset,
                                                    gdata,
                                                    resolutions['coarse'],
                                                    resolutions['fine'],
                                                    dims,
                                                    coarse_level = True)

    dc_verts={'fine':dc_verts_fine,
              'coarse':dc_verts_coarse}

    dc_edges={'fine':dc_edges_fine,
              'coarse':dc_edges_coarse}

    return dc_verts, dc_edges


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, gdata, res, res_fine, dims, coarse_level):
    # Compute vertices
    dc_verts = []
    vindex = {}
    dc_manifold_nodes = []
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
            c = is_inside(data, key)
            quad_signs.append(c)

        if all(quad_signs) or not any(quad_signs):
            continue

        # #this checks for certain problematic cases and introduces manifold nodes, if necessary
        # if coarse_level:
        #     if quad_signs == [False, True, False, True] or quad_signs == [True, False, True, False]:
        #         key = tuple(o)
        #         manifold_index[key] = len(dc_manifold_nodes)
        #         dc_manifold_nodes.append(ManifoldNode(o, quad_sign_keys, data, res))

        # Estimate hermite data
        h_data = []
        for e in quad_edges:
            if quad_signs[e[0]] != quad_signs[e[1]]:
                v0 = o + quad_verts[e[0]]*res
                v1 = o + quad_verts[e[1]]*res
                x, dx = estimate_hermite(data, gdata, v0, v1, res, res_fine, coarse_level)
                #h_data.append(x)
                h_data.append(tuple([x,dx]))
                print "zero crossing from node "+str(v0)+" to "+str(v1)
                print "\tx:\t"+str(x)
                print "\tdx:\t"+str(dx)

        #Solve qef to get vertex
        A = [n for p, n in h_data]
        b = [np.dot(p, n) for p, n in h_data]
        print A
        print b
        #quit()
        v, residue, rank, s = la.lstsq(A, b)

        # counter = 0
        # v = np.array([0.0, 0.0])
        #
        # for p in h_data:
        #     v += np.array(p)
        #     counter += 1
        #
        # v /= 1.0 * counter

        #Throw out failed solutions
        if la.norm(v-o) > 2 * res:
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

    if coarse_level: # if we are working on coarse scale we want to resolve non manifold vertices
        dc_verts, dc_edges = resolve_manifold_nodes(dc_edges, dc_verts, vindex, dc_manifold_nodes, manifold_index, res, dims)

    return np.array(dc_verts), np.array(dc_edges)