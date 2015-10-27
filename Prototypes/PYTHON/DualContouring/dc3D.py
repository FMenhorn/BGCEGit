# from __future__ import division
from operator import pos

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools as it
from dcHelpers import resolve_manifold_edges, create_manifold_edges
from MeshManager import MeshManager

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
cube_edges = [
    [k for (k, v) in enumerate(cube_verts) if v[i] == a and v[j] == b]
    for a in range(2)
    for b in range(2)
    for i in range(3)
    for j in range(3) if i != j]


# Use non-linear root finding to compute intersection point
def estimate_hermite(data, v0, v1):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    return x0


def tworesolution_dual_contour(dataset, resolutions, dims):
    Fine = dual_contour(dataset, resolutions['fine'],dims, coarse_level=False)

    Coarse = dual_contour(dataset,resolutions['coarse'],dims, coarse_level=True)

    return Fine,Coarse


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, dims, coarse_level):
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
                h_data.append(estimate_hermite(data, o + cube_verts[e[0]] * res, o + cube_verts[e[1]] * res))

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
    #New Object that manages the indices and the quad/vert list
    mesh=MeshManager(_quadlist=dc_quads,_vertlist=dc_verts,_data=data,_res=res,_vindex=vindex)
    if coarse_level:
        mesh = resolve_manifold_edges(mesh)
    mesh.verts=np.array(mesh.verts)
    return mesh