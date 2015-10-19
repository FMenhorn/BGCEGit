__author__ = 'benjamin'

from ManifoldEdge import ManifoldEdge
import numpy as np

# exports a np.ndarray to a csv file
def export_as_csv(data,name):
    import csv

    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(np.array(d))


def export_as_stl(quads_out_dc, verts_out_dc, plot_scale, filename):
    faces = []
    for q in quads_out_dc[plot_scale]:
        vtx = verts_out_dc[plot_scale][q]
        face = []
        for v in vtx:
            face.append(tuple(v))
        faces.append(face)

    import stlWrite
    with open(filename, 'wb') as fp:
        writer = stlWrite.ASCII_STL_Writer(fp)
        writer.add_faces(faces)
        writer.close()


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


# creates a list of manifold edges in a quad surface
def create_manifold_edges(_dc_quads, _dc_vindex, _dataset, _resolution):
    edge_usage_list = {}  # here we save the quads using a certain edge

    for i in range(_dc_quads.__len__()):  # traverse all quads
        q = _dc_quads[i]  # choose one quad
        edges = [(q[0], q[1]),  # edges of this quad
                 (q[1], q[2]),
                 (q[2], q[3]),
                 (q[3], q[0])]

        edge_keys = []  # keys of the edges
        for e in edges:  # traverse all edges of the quad
            key = tuple(sorted(e))  # calculate corresponding edge key.
            # Keys are made up of the vertex indices belonging to the edge (ascending order!)
            edge_keys.append(key)  # add to key list

        for e in edge_keys:  # traverse all keys of this quad
            if e in edge_usage_list:  # if the key is already in global list
                edge_usage_list[e].append(i)  # append current quad id, since quad is using this edge
            else:
                edge_usage_list[e] = [i]  # add key to list and save quad id, since quad is using this edge

    manifold_edges = {}  # here we save all the edges which are connected to more than two quads (manifold edges)
    manifold_edge_set = set()
    for e_u in edge_usage_list:  # traverse edge usage list
        if edge_usage_list[e_u].__len__() > 2:  # edges with more than 2 quads are manifold edges
            manifold_edge_set.add(e_u)

    for m_e in manifold_edge_set:
        vertex_usage_list = {m_e[0]: [], m_e[
            1]: []}  # here we save the quads using one of the two vertices of the manifold edge
        for v in m_e:  # traverse all (two) vertices in the edge
            for q_idx in range(_dc_quads.__len__()):  # traverse all quads
                q = _dc_quads[q_idx]  # current quad
                if (v in q) and (
                    q_idx not in edge_usage_list[m_e]):  # if one vertex (and not both!) is used by quad
                    vertex_usage_list[v].append(q_idx)  # add to vertex_usage_list
        # create ManifoldEdge in manifold_edge list with key corresponding to the manifold edge
        manifold_edges[m_e] = ManifoldEdge(m_e, edge_usage_list[m_e], vertex_usage_list, _dc_vindex, _dataset,
                                           _resolution, manifold_edge_set)

    return manifold_edges


# resolves manifold edges in a quad surface. After this step no more manifold edges occur in the surface and the surface
# is still closed and conforming.
def resolve_manifold_edges(_dc_verts, _dc_vindex, _dc_quads, _data, _resolution):
    manifold_edges = create_manifold_edges(_dc_quads, _dc_vindex, _data, _resolution)
    new_quads_list = []
    delete_quads_list = []

    for manifold_edge_key, manifold_edge in manifold_edges.items():
        new_quads, delete_quads = manifold_edge.resolve(_data, _dc_vindex, _dc_quads)
        new_quads_list += new_quads
        delete_quads_list += delete_quads

    _dc_quads = update_quad_list(_dc_quads, new_quads_list, delete_quads_list)

    return _dc_quads, manifold_edges


# updates the quad list by adding new quads from manifold resolution and deleting quads, which are not needed anymore
def update_quad_list(_dc_quads, new_quads_list, delete_quads_list):
    for i in delete_quads_list:
        _dc_quads[i] = None
    while None in _dc_quads:
        _dc_quads.remove(None)
    _dc_quads += new_quads_list
    return _dc_quads

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


