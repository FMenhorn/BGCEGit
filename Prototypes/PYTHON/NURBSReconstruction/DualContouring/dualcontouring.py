import numpy as np
import numpy.linalg as la
import itertools as it
from dcHelpers import resolve_manifold_edges, create_manifold_edges
from VoxelDataset import VoxelDataset

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
cube_edges = [[0, 1], [0, 2], [1, 3], [2, 3],
              [4, 6], [4, 5], [6, 7], [5, 7],
              [1, 5], [3, 7], [0, 4], [2, 6]]


def coarsen_dataset(coarsening_steps, fine_dataset):
    coarsening_threshold = 0.125

    if coarsening_steps > 0:
        # calculate coarse resolution
        coarse_res = 2 * fine_dataset._resolution

        # shrinking dimensions in coarsening step
        coarse_dims = {'min': 3 * [None], 'max': 3 * [None]}
        for d in range(3):
            coarse_dims['min'][d] = fine_dataset._dimensions['min'][d] + .5 * fine_dataset._resolution
            coarse_dims['max'][d] = fine_dataset._dimensions['max'][d] - .5 * fine_dataset._resolution

        coarse_data = set()
        # traverse all cells (each one has 4 datavalues) and combine all 4 values into one
        for x, y, z in fine_dataset.get_grid_iterator():
            o = np.array([float(x), float(y), float(z)])

            new_data = []
            for v in cube_verts:
                position = (o + v * fine_dataset._resolution)
                key = tuple(position)
                if fine_dataset.value_at(key):
                    coarse_data.add(key)
                    c = 1.0
                else:
                    c = 0.0
                new_data.append(c)

            new_o = o + .5 * fine_dataset._resolution * np.array([1, 1, 1])
            key = tuple(new_o)

            if np.mean(new_data) > coarsening_threshold:
                coarse_data.add(key)
            elif key in coarse_data:
                coarse_data.remove(key)

        coarse_dataset = VoxelDataset(coarse_dims, coarse_res, coarse_data)
        # recursively coarsen
        return coarsen_dataset(coarsening_steps - 1, coarse_dataset)
    else:
        # on last level surround structure with empty cells by extending dims
        coarse_dims = {'min': 3 * [None], 'max': 3 * [None]}
        for d in range(3):
            coarse_dims['min'][d] = fine_dataset._dimensions['min'][d] - .5 * fine_dataset._resolution
            coarse_dims['max'][d] = fine_dataset._dimensions['max'][d] + .5 * fine_dataset._resolution

        coarse_dataset = VoxelDataset(coarse_dims, fine_dataset._resolution, fine_dataset._dataset)

        return coarse_dataset


# Use non-linear root finding to compute intersection point
def estimate_hermite_easy(data, v0, v1, res, res_fine, coarse_level):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    return x0


def estimate_hermite(data, v0, v1, res, res_fine, coarse_level):
    data_v0 = data[tuple(v0)]
    data_v1 = data[tuple(v1)]

    if coarse_level:
        res_min = res_fine * 2
    else:
        res_min = res

    x0 = .5 * (v0 + v1)
    while res != res_min:
        data_x0 = data[tuple(x0)]
        if data_v0 != data_x0:
            v1 = x0
        elif data_v1 != data_x0:
            v0 = x0
        else:
            raise Exception("something wrong in bisection!")
        x0 = .5 * (v0 + v1)
        res /= 2.0

    return x0


def tworesolution_dual_contour(dataset, resolutions, dims):
    print "fine resolution:"
    print resolutions['fine']
    print dims
    fine_dataset = VoxelDataset(dims, resolutions['fine'], dataset)
    [dc_verts_fine, dc_quads_fine, dc_manifold_edges_fine] = dual_contour(fine_dataset,
                                                                          resolutions['fine'],
                                                                          is_coarse_level=False,
                                                                          do_manifold_treatment=False)

    # compute necessary coarsening steps from given coarse resolution.
    print "coarsening:"
    coarsening_steps = int(np.log(resolutions['coarse']) / np.log(2))
    assert coarsening_steps > 0  # at least one coarsening step has to be done!
    assert type(coarsening_steps) is int  # coarsening steps have to be integer!

    coarse_dataset = coarsen_dataset(coarsening_steps, fine_dataset)

    print "coarse resolution:"
    [dc_verts_coarse, dc_quads_coarse, dc_manifold_edges_coarse] = dual_contour(coarse_dataset,
                                                                                resolutions['fine'],
                                                                                is_coarse_level=True,
                                                                                do_manifold_treatment=True)

    dc_verts = {'fine': dc_verts_fine, 'coarse': dc_verts_coarse}
    dc_quads = {'fine': dc_quads_fine, 'coarse': dc_quads_coarse}
    dc_manifolds = {'fine': dc_manifold_edges_fine, 'coarse': dc_manifold_edges_coarse}

    datasets = {'fine': fine_dataset, 'coarse': coarse_dataset}

    return dc_verts, dc_quads, dc_manifolds, datasets


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(dataset, res_fine, is_coarse_level, do_manifold_treatment):
    # Compute vertices
    dc_verts = []
    vindex = {}

    for x, y, z in dataset.get_grid_iterator():

        o = np.array([float(x), float(y), float(z)])

        cube_signs = []
        # Get signs for cube
        for v in cube_verts:
            position = (o + v * dataset._resolution)
            key = tuple(position)
            c = True
            if dataset.valid_point(key):
                c = dataset[key]
            cube_signs.append(c)

        if all(cube_signs) or not any(cube_signs):
            continue

        # Estimate hermite data
        h_data = []
        for e in cube_edges:
            if cube_signs[e[0]] != cube_signs[e[1]]:
                h_data.append(estimate_hermite(dataset, o + cube_verts[e[0]] * dataset._resolution,
                                               o + cube_verts[e[1]] * dataset._resolution, dataset._resolution,
                                               res_fine, is_coarse_level))

        counter = 0
        v = np.array([0.0, 0.0, 0.0])

        for p in h_data:
            v += np.array(p)
            counter += 1

        v /= 1.0 * counter

        # Throw out failed solutions
        if la.norm(v - o) > 2 * dataset._resolution:
            continue

        # Emit one vertex per every cube that crosses
        vindex[tuple(o)] = len(dc_verts)
        dc_verts.append(v)

    # Construct faces
    dc_quads = []
    for x, y, z in dataset.get_grid_iterator():
        if not (x, y, z) in vindex:
            continue

        # Emit one edge per each edge that crosses
        o = np.array([float(x), float(y), float(z)])
        for i in range(3):
            for j in range(i):
                if tuple(o + dataset._resolution * dirs[i]) in vindex and \
                                tuple(o + dataset._resolution * dirs[j]) in vindex and \
                                tuple(o + dataset._resolution * (dirs[i] + dirs[j])) \
                                in vindex:
                    k = 3 - (i + j)  # normal id
                    c = True
                    d = True
                    key_ij = tuple(o + dataset._resolution * dirs[i] + dataset._resolution * dirs[j])
                    key_ijk = tuple(
                        o + dataset._resolution * dirs[i] + dataset._resolution * dirs[j] + dataset._resolution * dirs[
                            k])
                    if dataset.point_is_inside(key_ij):
                        c = dataset[key_ij]
                    if dataset.point_is_inside(key_ijk):
                        d = dataset[key_ijk]
                    if c != d:
                        dc_quads.append([vindex[tuple(o)], vindex[tuple(o + dataset._resolution * dirs[i])],
                                         vindex[
                                             tuple(o + dataset._resolution * dirs[i] + dataset._resolution * dirs[j])],
                                         vindex[tuple(o + dataset._resolution * dirs[j])]])

    if do_manifold_treatment:
        dc_verts, dc_quads, dc_manifold_edges = resolve_manifold_edges(dc_verts, vindex, dc_quads, dataset,
                                                                       dataset._resolution)
    else:
        dc_manifold_edges = create_manifold_edges(dc_quads, vindex, dataset, dataset._resolution)

    return np.array(dc_verts), np.array(dc_quads), dc_manifold_edges
