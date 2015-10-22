__author__ = 'benjamin'

import numpy as np

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


def update_mesh_2d(dc_verts, dc_edges, new_edges_list, new_nodes_list, delete_edges_list):
    dc_verts += new_nodes_list # append new nodes
    dc_edges += new_edges_list # append new edges

    for edge_idx in delete_edges_list: # delete edges not needed anymore
        dc_edges[edge_idx] = None
    for i in delete_edges_list:
        dc_edges[i] = None
    while None in dc_edges:
        dc_edges.remove(None)

    return dc_verts, dc_edges


def generate_vertex_usage_dict(dc_edges):
    vertex_usage_dict = {}  # here we save the edges using a certain node

    for i in range(dc_edges.__len__()):  # traverse all edges
        nodes = dc_edges[i]  # choose one edge

        for n in nodes:  # traverse all nodes of this edge
            if n in vertex_usage_dict:  # if the key is already in global list
                vertex_usage_dict[n].append(i)  # append current edge id, since edge is using this node
            else:
                vertex_usage_dict[n] = [i]  # add key to list and save edge id, since edge is using this node

    return vertex_usage_dict


