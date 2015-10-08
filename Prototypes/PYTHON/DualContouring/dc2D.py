# from __future__ import division
from operator import pos

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools as it

# Cardinal directions
from skimage.morphology.selem import cube

dirs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]

# Vertices of quad
quad_verts = [np.array([x, y])
                   for x in np.arange(0,2,1.0)
                   for y in np.arange(0,2,1.0)]

# Edges of quad
quad_edges = [[0,1],[0,2],[1,3],[2,3]]

# Use non-linear root finding to compute intersection point
def estimate_hermite(data, v0, v1):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    #print 'x0='+str(v0)
    #print 'x1='+str(v1)
    return x0


def tworesolution_dual_contour(dataset,resolutions,dims):
    [dc_verts_fine,dc_edges_fine]=dual_contour(dataset,resolutions['fine'],dims)
    [dc_verts_coarse,dc_edges_coarse]=dual_contour(dataset,resolutions['coarse'],dims)

    dc_verts={'fine':dc_verts_fine,'coarse':dc_verts_coarse}
    dc_edges={'fine':dc_edges_fine,'coarse':dc_edges_coarse}

    return dc_verts, dc_edges


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data,res,dims):
    # Compute vertices
    dc_verts = []
    vindex = {}
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
        o = np.array([float(x), float(y)])

        quad_signs=[]
        # Get signs for cube
        for v in quad_verts:
            position = (o + v*res)
            key = tuple(position)
            quad_signs.append(data[key] > 0)

        #print "voxel at "+str(o)+": "+str(quad_signs)

        if all(quad_signs) or not any(quad_signs):
            continue

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
        vindex[tuple(o)] = len(dc_verts)
        dc_verts.append(v)

    # Construct faces
    dc_edges = []
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res)):
        if not (x, y) in vindex:
            continue

        # Emit one edge per each edge that crosses
        o = np.array([float(x), float(y)])
        for i in range(2):
            if tuple(o + res*dirs[i]) in vindex:
                if (data[tuple(o+res*dirs[i]+res*dirs[int(not i)])] > 0) != (data[tuple(o+res*dirs[i])] > 0):
                    dc_edges.append([vindex[tuple(o)], vindex[tuple(o + np.array(dirs[i])*res)]])

    return dc_verts, dc_edges


def export_as_csv(data,name):
    import csv
    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(np.array(d))


def sample_data(f, res, dims):
    data = {}
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax']+res, res), np.arange(dims['ymin'], dims['ymax']+res, res)):
        key = (x, y)
        x_vec = np.array([x, y])
        data[key] = f(x_vec)
    return data


def data_to_voxel(_data, res, dims):
    length = (dims['xmax']-dims['xmin'])
    height = (dims['ymax']-dims['ymin'])

    voxels_mat = np.empty([length/res+1,height/res+1])
    x_mat = np.empty([length/res+1,height/res+1])
    y_mat = np.empty([length/res+1,height/res+1])
    for i in range(int(length/res+1)):
        for j in range(int(height/res+1)):
            thisX = dims['xmin']+i*res
            thisY = dims['ymin']+j*res
            voxels_mat[i,j]=int(_data[tuple(np.array([thisX,thisY]))] > 0)
            x_mat[i,j] = thisX
            y_mat[i,j] = thisY

    return voxels_mat,x_mat,y_mat


def test_f(x):
    center = np.array([4.0, 4.0])
    radius = 2.0
    d = x - center
    return np.dot(d, d) - radius ** 2


dimensions = {'xmin':0,'xmax':8,'ymin':0,'ymax':8}
res_fine = 1.0/8.0
res_coarse = res_fine * 16.0
resolutions = {'fine':res_fine,'coarse':res_coarse}

data = sample_data(test_f,resolutions['fine'],dimensions)
[voxels_fine,x_mat_fine,y_mat_fine] = data_to_voxel(data,resolutions['fine'],dimensions)
[voxels_coarse,x_mat_coarse,y_mat_coarse] = data_to_voxel(data,resolutions['coarse'],dimensions)

[verts, edges] = tworesolution_dual_contour(data, resolutions, dimensions)

export_as_csv(verts['fine'],'verts_fine')
export_as_csv(edges['fine'],'edges_fine')
export_as_csv(voxels_fine,'voxels_fine')
export_as_csv(x_mat_fine,'x_mat_fine')
export_as_csv(y_mat_fine,'y_mat_fine')

export_as_csv(verts['coarse'],'verts_coarse')
export_as_csv(edges['coarse'],'edges_coarse')
export_as_csv(voxels_coarse,'voxels_coarse')
export_as_csv(x_mat_coarse,'x_mat_coarse')
export_as_csv(y_mat_coarse,'y_mat_coarse')