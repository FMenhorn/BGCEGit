import numpy as np
import numpy.linalg as la
import itertools as it
from dcHelpers import resolve_manifold_edges, is_inside, create_manifold_edges

#########################
#### DUAL CONTOURING ####
#########################

dirs = [np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0])]

# Vertices of cube
cube_verts = [np.array([x, y, z])
              for x in range(2)
              for y in range(2)
              for z in range(2)]

# Edges of cube
cube_edges = [[0,1],[0,2],[1,3],[2,3],
              [4,6],[4,5],[6,7],[5,7],
              [1,5],[3,7],[0,4],[2,6]]


def coarsen_dataset(coarsening_steps, fine_dataset, res, dims):
    if coarsening_steps > 0:
        coarse_res = 2.0 * res
        #shrinking dimensions in coarsening step
        coarse_dims={}
        coarse_dims['xmin']=dims['xmin']+.5 * res
        coarse_dims['xmax']=dims['xmax']-.5 * res
        coarse_dims['ymin']=dims['ymin']+.5 * res
        coarse_dims['ymax']=dims['ymax']-.5 * res
        coarse_dims['zmin']=dims['zmin']+.5 * res
        coarse_dims['zmax']=dims['zmax']-.5 * res

        coarse_dataset = {}
        # traverse all cells (each one has 4 datavalues) and combine all 4 values into one
        for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res),
                                  np.arange(dims['ymin'], dims['ymax'], res),
                                  np.arange(dims['zmin'], dims['zmax'], res)):
            o = np.array([float(x), float(y), float(z)])

            new_data = []
            for v in cube_verts:
                position = (o + v * res)
                key = tuple(position)
                if key in fine_dataset:
                    c = 1.0
                else:
                    c = 0.0
                new_data.append(c)

            new_o = o+.5*res*np.array([1,1,1])
            key = tuple(new_o)

            if np.mean(new_data) > 0.125:
                coarse_dataset[key] = -1

        #recursively coarsen
        return coarsen_dataset(coarsening_steps-1, coarse_dataset, coarse_res, coarse_dims)
    else:
        #on last level surround structure with empty cells by extending dims
        dims['xmin']=dims['xmin']-.5 * res
        dims['xmax']=dims['xmax']+.5 * res
        dims['ymin']=dims['ymin']-.5 * res
        dims['ymax']=dims['ymax']+.5 * res
        dims['zmin']=dims['zmin']-.5 * res
        dims['zmax']=dims['zmax']+.5 * res

        return fine_dataset, res, dims

# Use non-linear root finding to compute intersection point
def estimate_hermite_easy(data, v0, v1, res, res_fine, coarse_level):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    return x0


def estimate_hermite(data, v0, v1, res, res_fine, coarse_level):
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

    return x0


def tworesolution_dual_contour(fine_dataset, resolutions, dims):
    [dc_verts_fine, dc_quads_fine, dc_manifold_edges_fine] = dual_contour(fine_dataset,
                                                                          resolutions['fine'],
                                                                          resolutions['fine'],
                                                                          dims,
                                                                          coarse_level=False,
                                                                          do_manifold_treatment=False)

    # compute necessary coarsening steps from given coarse resolution.
    coarsening_steps = int(np.log(resolutions['coarse'])/np.log(2))
    coarse_dataset, coarse_res, coarse_dims = coarsen_dataset(coarsening_steps,
                                                              fine_dataset,
                                                              resolutions['fine'],
                                                              dims)

    [dc_verts_coarse, dc_quads_coarse, dc_manifold_edges_coarse] = dual_contour(coarse_dataset,
                                                                                coarse_res,
                                                                                resolutions['fine'],
                                                                                coarse_dims,
                                                                                coarse_level=True,
                                                                                do_manifold_treatment=True)

    dc_verts = {'fine': dc_verts_fine, 'coarse': dc_verts_coarse}
    dc_quads = {'fine': dc_quads_fine, 'coarse': dc_quads_coarse}
    dc_manifolds = {'fine': dc_manifold_edges_fine, 'coarse': dc_manifold_edges_coarse}

    return dc_verts, dc_quads, dc_manifolds


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, res_fine, dims, coarse_level, do_manifold_treatment):
    # Compute vertices
    dc_verts = []
    vindex = {}
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res),
                              np.arange(dims['zmin'], dims['zmax'], res)):
        o = np.array([float(x), float(y), float(z)])

        cube_signs = []
        # Get signs for cube
        for v in cube_verts:
            position = (o + v * res)
            key = tuple(position)
            c = True
            if key in data:
                c = data[key] > 0
            cube_signs.append(c)

        if all(cube_signs) or not any(cube_signs):
            continue

        # Estimate hermite data
        h_data = []
        for e in cube_edges:
            if cube_signs[e[0]] != cube_signs[e[1]]:
                h_data.append(estimate_hermite(data, o + cube_verts[e[0]] * res, o + cube_verts[e[1]] * res, res, res_fine, coarse_level))

        counter = 0
        v = np.array([0.0, 0.0, 0.0])

        for p in h_data:
            v += np.array(p)
            counter += 1

        v /= 1.0 * counter

        # Throw out failed solutions
        if la.norm(v - o) > 2 * res:
            continue

        # Emit one vertex per every cube that crosses
        vindex[tuple(o)] = len(dc_verts)
        dc_verts.append(v)

    # Construct faces
    dc_quads = []
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res),
                              np.arange(dims['zmin'], dims['zmax'], res)):
        if not (x, y, z) in vindex:
            continue

        # Emit one edge per each edge that crosses
        o = np.array([float(x), float(y), float(z)])
        for i in range(3):
            for j in range(i):
                if tuple(o + res * dirs[i]) in vindex and tuple(o + res * dirs[j]) in vindex and tuple(
                                o + res * (dirs[i] + dirs[j])) in vindex:
                    k = 3 - (i + j)  # normal id
                    c = True
                    d = True
                    key_ij = tuple(o + res * dirs[i] + res * dirs[j])
                    key_ijk = tuple(o + res * dirs[i] + res * dirs[j] + res * dirs[k])
                    if key_ij in data:
                        c = data[key_ij] > 0
                    if key_ijk in data:
                        d = data[key_ijk] > 0
                    if c != d:
                        dc_quads.append([vindex[tuple(o)], vindex[tuple(o + res * dirs[i])],
                                         vindex[tuple(o + res * dirs[i] + res * dirs[j])],
                                         vindex[tuple(o + res * dirs[j])]])

    if do_manifold_treatment:
        dc_verts, dc_quads, dc_manifold_edges = resolve_manifold_edges(dc_verts, vindex, dc_quads, data, res)
    else:
        dc_manifold_edges = create_manifold_edges(dc_quads, vindex, data, res)

    return np.array(dc_verts), np.array(dc_quads), dc_manifold_edges
