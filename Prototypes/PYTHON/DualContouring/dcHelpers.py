from ManifoldEdge import ManifoldEdge
import numpy as np

__author__ = 'benjamin'


##############
# 3D HELPERS #
##############

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
def create_manifold_edges(_mesh):
    edge_usage_dict = _mesh.generate_edge_usage_dict()  # here we save the quads using a certain edge

    manifold_edges = {}  # here we save all the edges which are connected to more than two quads (manifold edges)
    manifold_edge_set = set()
    for e_u in edge_usage_dict:  # traverse edge usage list
        if edge_usage_dict[e_u].__len__() > 2:  # edges with more than 2 quads are manifold edges
            manifold_edge_set.add(e_u)

    for m_e in manifold_edge_set:
        # here we save the quads using one of the two vertices of the manifold edge
        vertex_usage_dict = {m_e[0]: [], m_e[1]: []}
        for v in m_e:  # traverse all (two) vertices in the edge
            for q_idx in range(_mesh.quadslen):  # traverse all quads
                q = _mesh.quads[q_idx]  # current quad
                if (v in q) and (q_idx not in edge_usage_dict[m_e]):  # if one vertex (and not both!) is used by quad
                    vertex_usage_dict[v].append(q_idx)  # add to vertex_usage_list
        # create ManifoldEdge in manifold_edge list with key corresponding to the manifold edge
        manifold_edges[m_e] = ManifoldEdge(_manifold_edge_key = m_e,
                                           _manifold_edge_quad_ids = edge_usage_dict[m_e],
                                           _manifold_vertex_quad_ids_dict = vertex_usage_dict,
                                           _mesh=_mesh,
                                           _manifold_edge_set = manifold_edge_set)

    return manifold_edges


# resolves manifold edges in a quad surface. After this step no more manifold edges occur in the surface and the surface
# is still closed and conforming.
def resolve_manifold_edges(_mesh):
    # create manifold edges for the whole surface
    manifold_edges = create_manifold_edges(_mesh)


    for manifold_edge_key, manifold_edge in manifold_edges.items():
        manifold_edge.resolve(_mesh)

    _mesh.update_mesh()

    edge_usage_dict = _mesh.generate_edge_usage_dict()  # here we save the quads using a certain edge

    not_consistent_edges = {}
    for edge, used in edge_usage_dict.items():
        if used.__len__() != 2:
            not_consistent_edges[edge] = used
    resolve_not_consistent(_mesh, not_consistent_edges)

    return _mesh

#TO DO: CHANGE
def resolve_not_consistent(_mesh, _not_consistent_edges):

    not_consistent_quad_clusters = []
    for edge, used in _not_consistent_edges.items():
        if used.__len__() == 4:
            not_consistent_quad_clusters.append(used)

    for cluster in not_consistent_quad_clusters:
        resolve_quad_cluster(_mesh,cluster)
        #o_idx_nodes = _mesh.quadslen
        #new_quads, new_nodes, delete_quads, o_idx_nodes = resolve_quad_cluster(_dc_quads, _dc_verts, cluster, o_idx_nodes)
        _mesh.update_mesh()



#TO DO: CHANGE
def resolve_quad_cluster(_mesh, _cluster):
    _mesh.delete_quad = list(_cluster) # all old quads will be removed

    quads = 4 * [None]  # quad with all vertex ids

    for i in range(4):
        c = _cluster[i]
        quads[i] = list(_mesh.quads[c])

    all_nodes = np.array(quads).reshape(16).tolist()
    new_node = np.zeros([3])
    for v_id in np.unique(all_nodes):
        vtx = _mesh.verts[v_id]
        new_node += vtx

    new_node /= 8.0

    new_nodes = [new_node]

    for q in quads:
        for i in range(4):
            if all_nodes.count(q[i])==1:
                unique_node = q[i]  # node only occouring in this quad (out of the four involved quads
                break
        tmp = q.index(unique_node)
        q[(tmp+2)%4] = _mesh.quadslen
        _mesh.add_quad(q)

    _mesh.quadslen +=1




