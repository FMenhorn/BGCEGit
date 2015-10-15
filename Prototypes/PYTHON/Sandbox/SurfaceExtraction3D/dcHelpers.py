__author__ = 'benjamin'


# exports a np.ndarray to a csv file
def export_as_csv(data,name):
    import csv

    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(np.array(d))


# transforms data to matrix format with [X,Y,Z,VoxelData]
def data_to_voxel(_data, res, dims):
    import numpy as np

    length = (dims['xmax']-dims['xmin'])
    height = (dims['ymax']-dims['ymin'])
    depth = (dims['zmax']-dims['zmin'])

    voxels_mat = np.empty([length/res+1,height/res+1,depth/res+1])
    x_mat = np.empty(voxels_mat.shape)
    y_mat = np.empty(voxels_mat.shape)
    z_mat = np.empty(voxels_mat.shape)
    for i in range(int(length/res+1)):
        for j in range(int(height/res+1)):
            for k in range(int(depth/res+1)):
                thisX = dims['xmin']+i*res
                thisY = dims['ymin']+j*res
                thisZ = dims['zmin']+k*res
                voxels_mat[i, j, k] = int(_data[tuple(np.array([thisX,thisY,thisZ]))] > 0)
                x_mat[i, j, k] = thisX
                y_mat[i, j, k] = thisY
                z_mat[i, j, k] = thisZ

    return voxels_mat,x_mat,y_mat,z_mat
