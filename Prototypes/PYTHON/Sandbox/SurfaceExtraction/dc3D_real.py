#DUAL CONTOURING 3D for the vtk data
import numpy as np
import numpy.linalg as la
import itertools as it


# Cardinal directions
dirs = [np.array([0.0,0.0,1.0]), np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0])]

# Vertices of cube
cube_verts = [np.array([x, y, z])
    for x in range(2)
    for y in range(2)
    for z in range(2)]

# Edges of cube
cube_edges = [
    [k for (k,v) in enumerate(cube_verts) if v[i] == a and v[j] == b]
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
    [dc_verts_fine,dc_quads_fine]=dual_contour(dataset,resolutions['fine'],dims)
    [dc_verts_coarse,dc_quads_coarse]=dual_contour(dataset,resolutions['coarse'],dims)

    dc_verts={'fine':dc_verts_fine,'coarse':dc_verts_coarse}
    dc_quads={'fine':dc_quads_fine,'coarse':dc_quads_coarse}

    return dc_verts, dc_quads


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, dims):
    # Compute vertices
    dc_verts = []
    vindex = {}


    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
        o = np.array([float(x), float(y), float(z)])

        cube_signs=[]
        # Get signs for cube
        for v in cube_verts:
            position = (o + v*res)
            key = tuple(position)
            c=True
            if key in data:
                c=False
            cube_signs.append(c)


        if all(cube_signs) or not any(cube_signs):
            continue

        # Estimate hermite data
        h_data = []
        for e in cube_edges:
            if cube_signs[e[0]] != cube_signs[e[1]]:
                h_data.append(estimate_hermite(data, o + cube_verts[e[0]]*res, o + cube_verts[e[1]]*res))

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
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
        if not (x, y, z) in vindex:
            continue

        # Emit one edge per each edge that crosses
        o = np.array([float(x), float(y), float(z)])
        for i in range(3):
            for j in range(i):
                if tuple(o + res*dirs[i]) in vindex and tuple(o + res*dirs[j]) in vindex and tuple(o + res*(dirs[i] + dirs[j])) in vindex:
                    k = 3-(i+j) # normal id
                    c=True
                    d=True
                    if tuple(o+res*dirs[i]+res*dirs[j]) in data:
                        c=False
                    if tuple(o+res*dirs[i]+res*dirs[j]+res*dirs[k]) in data:
                        d=False
                    #if (data[tuple(o+res*dirs[i]+res*dirs[j])] > 0) != (data[tuple(o+res*dirs[i]+res*dirs[j]+res*dirs[k])] > 0): # dir[i]+dir[j]+dir[k] = [1,1,1] for all!
                    if c != d:
                        dc_quads.append([vindex[tuple(o)], vindex[tuple(o+res*dirs[i])], vindex[tuple(o+res*dirs[i]+res*dirs[j])], vindex[tuple(o+res*dirs[j])]])

    return np.array(dc_verts), np.array(dc_quads)


def export_as_csv(data,name):
    import csv
    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(np.array(d))




#res_fine = 0.125
#res_coarse = res_fine * 4.0
#resolutions = {'fine':res_fine,'coarse':res_coarse}

#TESTING VTK DATA

#fine_data = sample_data(doubletorus_f, resolutions['fine'], dimensions)
#[voxels_fine, x_mat_fine, y_mat_fine, z_mat_fine] = data_to_voxel(fine_data,resolutions['fine'],dimensions)
#[voxels_coarse, x_mat_coarse, y_mat_coarse, z_mat_coarse] = data_to_voxel(fine_data,resolutions['coarse'],dimensions)

#[verts, quads] = tworesolution_dual_contour(fine_data, resolutions, dimensions)

#export_as_csv(verts['fine'], 'verts_fine')
#export_as_csv(quads['fine'], 'quads_fine')
#export_as_csv(voxels_fine, 'voxels_fine')
#export_as_csv(x_mat_fine, 'x_mat_fine')
#export_as_csv(y_mat_fine, 'y_mat_fine')
#export_as_csv(z_mat_fine, 'z_mat_fine')

#export_as_csv(verts['coarse'], 'verts_coarse')
#export_as_csv(quads['coarse'], 'quads_coarse')
#export_as_csv(voxels_coarse, 'voxels_coarse')
#export_as_csv(x_mat_coarse, 'x_mat_coarse')
#export_as_csv(z_mat_coarse, 'z_mat_coarse')

