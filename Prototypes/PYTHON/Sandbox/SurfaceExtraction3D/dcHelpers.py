from ManifoldEdge import ManifoldEdge
import numpy as np
import itertools as it
import stlWrite

from quadHelpers import *

__author__ = 'benjamin'

###################
# GENERAL HELPERS #
###################

def is_inside(data, key):
    c = True
    if key in data:
        c = data[key] > 0
    return c

# exports a np.ndarray to a csv file
def export_as_csv(data,name):
    import csv

    with open(name+'.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            csvwriter.writerow(np.array(d))


##############
# 2D HELPERS #
##############


# resolves manifold nodes in a spline contour. After this step no more manifold nodes occur in the contour and the
# contour is still closed.
def resolve_manifold_nodes(_dc_edges, _dc_verts, _dc_vindex, _dc_manifold_nodes, _dc_manifold_index, _resolution, _dimensions):
    # here we store, which vertices are uses by which edges. If one vertex is used by more than 2 edges, it is a
    # non-manifold vertex
    vertex_usage_dict = generate_vertex_usage_dict(_dc_edges)

    # in those lists we save the edges/nodes added and edges deleted after resolving the manifold vertices. We do
    # not want to do this on the fly, because otherwise the references to vertices will as well as to edges would be
    # changing all the time.
    new_edges_list = []
    new_nodes_list = []
    delete_edges_list = []

    # save index origin in the node list. New nodes created in the following process will be appended to the node
    # list and therefore edges referencing those nodes need to know thoses nodes
    o_idx_nodes =  _dc_verts.__len__()
    for x, y in it.product(np.arange(_dimensions['xmin'], _dimensions['xmax'], _resolution),
                           np.arange(_dimensions['ymin'], _dimensions['ymax'], _resolution)):
        if (x, y) in _dc_manifold_index: # if the current voxel holds a non manifold node
            i = _dc_manifold_index[(x, y)]
            global_idx = _dc_vindex[(x, y)]
            # resolve this node. This means splitting it and correctly changing the references to its children
            new_edges, new_nodes, delete_edges, o_idx_nodes = _dc_manifold_nodes[i].resolve(o_idx_nodes,
                                                                                            global_idx,
                                                                                            _dc_vindex,
                                                                                            vertex_usage_dict)
            # append new edges/nodes and delete edges introduced by resolution of this node to globally needed
            # additions and deletions
            new_edges_list += new_edges
            new_nodes_list += new_nodes
            delete_edges_list += delete_edges

    # update mesh by deleting edges, which have to be deleted and adding new edges/nodes. No nodes are deleted at
    # all! If a node is not referenced by any edge, it is not part of the mesh anymore, but still it remains in the
    # node list. Otherwise we would have to change all the references from the edges, because all the vertex indices
    # can change upon deletion of one vertex. One could delete superfluous nodes in a postprocessing step, anyhow.
    [_dc_verts, _dc_edges] = update_mesh_2d(_dc_verts, _dc_edges, new_edges_list, new_nodes_list, delete_edges_list)

    return _dc_verts, _dc_edges


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


##############
# 3D HELPERS #
##############


# exports a mesh to stl
def export_as_stl(quads_out_dc, verts_out_dc, plot_scale, filename):
    faces = []
    for q in quads_out_dc[plot_scale]:
        vtx = verts_out_dc[plot_scale][q]
        face = []
        for v in vtx:
            face.append(tuple(v))
        faces.append(face)

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


def generate_edge_usage_dict(_dc_quads):
    edge_usage_dict = {}  # here we save the quads using a certain edge

    for i in range(_dc_quads.__len__()):  # traverse all quads
        q = _dc_quads[i]  # choose one quad

        edge_keys = get_quad_edge_list(q) # keys of the edges

        for e in edge_keys:  # traverse all keys of this quad
            if e in edge_usage_dict:  # if the key is already in global list
                edge_usage_dict[e].append(i)  # append current quad id, since quad is using this edge
            else:
                edge_usage_dict[e] = [i]  # add key to list and save quad id, since quad is using this edge

    return edge_usage_dict


# creates a list of manifold edges in a quad surface
def create_manifold_edges(_dc_quads, _dc_vindex, _dataset, _resolution):
    edge_usage_dict = generate_edge_usage_dict(_dc_quads)  # here we save the quads using a certain edge

    manifold_edges = {}  # here we save all the edges which are connected to more than two quads (manifold edges)
    manifold_edge_set = set()
    for e_u in edge_usage_dict:  # traverse edge usage list
        if edge_usage_dict[e_u].__len__() > 2:  # edges with more than 2 quads are manifold edges
            manifold_edge_set.add(e_u)

    for m_e in manifold_edge_set:
        # here we save the quads using one of the two vertices of the manifold edge
        vertex_usage_dict = {m_e[0]: [], m_e[1]: []}
        for v in m_e:  # traverse all (two) vertices in the edge
            for q_idx in range(_dc_quads.__len__()):  # traverse all quads
                q = _dc_quads[q_idx]  # current quad
                if (v in q) and (q_idx not in edge_usage_dict[m_e]):  # if one vertex (and not both!) is used by quad
                    vertex_usage_dict[v].append(q_idx)  # add to vertex_usage_list
        # create ManifoldEdge in manifold_edge list with key corresponding to the manifold edge
        manifold_edges[m_e] = ManifoldEdge(_manifold_edge_key = m_e,
                                           _manifold_edge_quad_ids = edge_usage_dict[m_e],
                                           _manifold_vertex_quad_ids_dict = vertex_usage_dict,
                                           _dc_vindex = _dc_vindex,
                                           _dataset = _dataset,
                                           _resolution = _resolution,
                                           _manifold_edge_set = manifold_edge_set)

    return manifold_edges


# resolves manifold edges in a quad surface. After this step no more manifold edges occur in the surface and the surface
# is still closed and conforming.
def resolve_manifold_edges(_dc_verts, _dc_vindex, _dc_quads, _data, _resolution):
    # create manifold edges for the whole surface
    manifold_edges = create_manifold_edges(_dc_quads, _dc_vindex, _data, _resolution)

    # in those lists we save the edges/nodes added and edges deleted after resolving the manifold vertices. We do
    # not want to do this on the fly, because otherwise the references to vertices will as well as to edges would be
    # changing all the time.
    new_nodes_list = []
    new_quads_list = []
    delete_quads_list = []

    # origin index of the vertex list
    o_idx_nodes = _dc_verts.__len__()

    # in this dict we will save the mapping from old indices of removed manifold vertices to their children
    vindex_mapping = {}

    for manifold_edge_key, manifold_edge in manifold_edges.items():
        new_quads, new_nodes, delete_quads, o_idx_nodes, vindex_mapping = manifold_edge.resolve(_data,
                                                                                                _dc_vindex,
                                                                                                _dc_quads,
                                                                                                _dc_verts,
                                                                                                o_idx_nodes,
                                                                                                vindex_mapping)
        new_nodes_list += new_nodes
        new_quads_list += new_quads
        delete_quads_list += delete_quads

    _dc_verts, _dc_quads = update_mesh_3d(_dc_verts,
                                          _dc_quads,
                                          new_quads_list,
                                          new_nodes_list,
                                          delete_quads_list)

    edge_usage_dict = generate_edge_usage_dict(_dc_quads)  # here we save the quads using a certain edge

    not_consistent_edges = {}
    for edge, used in edge_usage_dict.items():
        if used.__len__() != 2:
            not_consistent_edges[edge] = used

    _dc_verts, _dc_quads = resolve_not_consistent(_dc_verts, _dc_quads, not_consistent_edges)

    return _dc_verts, _dc_quads


def resolve_not_consistent(_dc_verts, _dc_quads, _not_consistent_edges):

    not_consistent_quad_clusters = []
    for edge, used in _not_consistent_edges.items():
        if used.__len__() == 4:
            not_consistent_quad_clusters.append(used)

    for cluster in not_consistent_quad_clusters:
        o_idx_nodes = _dc_verts.__len__()
        new_quads, new_nodes, delete_quads, o_idx_nodes = resolve_quad_cluster(_dc_quads, _dc_verts, cluster, o_idx_nodes)
        _dc_verts, _dc_quads = update_mesh_3d(_dc_verts, _dc_quads, new_quads, new_nodes, delete_quads)

    return _dc_verts, _dc_quads


def resolve_quad_cluster(_dc_quads, _dc_verts, _cluster, o_idx_nodes):
    new_quads = []
    new_nodes = []
    delete_quads = list(_cluster) # all old quads will be removed

    quads = 4 * [None]  # quad with all vertex ids

    for i in range(4):
        c = _cluster[i]
        quads[i] = list(_dc_quads[c])

    all_nodes = np.array(quads).reshape(16).tolist()

    new_node = np.zeros([3])
    for v_id in np.unique(quads):
        vtx = _dc_verts[v_id]
        new_node += vtx

    new_node /= 8.0

    new_nodes = [new_node]

    for q in quads:
        for i in range(4):
            if all_nodes.count(q[i])==1:
                unique_node = q[i]  # node only occouring in this quad (out of the four involved quads
                break
        tmp = q.index(unique_node)
        q[(tmp+2)%4] = o_idx_nodes
        new_quads.append(q)

    o_idx_nodes +=1

    return new_quads, new_nodes, delete_quads, o_idx_nodes


def update_mesh_3d(_dc_verts, _dc_quads, _new_quads_list, _new_nodes_list, _delete_quads_list):
    _dc_verts += _new_nodes_list # append new nodes
    _dc_quads += _new_quads_list # append new quads

    for edge_idx in _delete_quads_list: # delete quads not needed anymore
        _dc_quads[edge_idx] = None
    for i in _delete_quads_list:
        _dc_quads[i] = None
    while None in _dc_quads:
        _dc_quads.remove(None)

    return _dc_verts, _dc_quads