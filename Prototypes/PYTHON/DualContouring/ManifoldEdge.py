import numpy as np
from quadHelpers import quad_has_edge

__author__ = 'benjamin'


class ManifoldEdge:
    def __init__(self, _manifold_edge_key, _manifold_edge_quad_ids, _manifold_vertex_quad_ids_dict, _dc_vindex, _dataset,
                 _resolution, _manifold_edge_set):
        # resolution of the grid
        self.resolution = _resolution

        # key corresponding to the vertices of the edge
        self.v_key = [None] * 2
        # indices corresponding to the vertices of the edge
        # access pattern v_idx[local_manifold_vertex_id] = global_vertex_id
        self.v_idx = _manifold_edge_key
        for i in range(2):
            self.v_key[i] = search_vertex_key_from_index(_dc_vindex, self.v_idx[i])

        # stores the indices of the child vertices of each manifold vertex after the edge is resolved
        # access pattern: v_children_idx[local_manifold_vertex_id][split_id] = global_vertex_id
        self.v_children_idx = [2 * [None] for _ in range(2)]

        # stores the edge keys of edges connected to the respective children after the edge is resolved
        # access pattern: v_children_edge_keys[local_manifold_vertex_id][split_id] = list of connected vertices
        self.v_children_connection_idx = [[ set() for _ in range(2)] for _ in range (2)]

        # direction vector of the edge (direction vertex0 -> vertex1) and corresponding dimensions
        self.edge_dir01, self.edge_dim = self.calculate_edge_dir01()

        # keys of neighbouring voxels and the directions
        self.neighbour_keys, self.neighbour_directions = self.calculate_neighbour_keys()

        # key of the datavalue at the middle of the face penetrated by the edge and the index [0] or [1] of the v_key
        # lying in that plane
        self.middle_value_key, self.middle_plane_index = self.calculate_middle_value_key()
        # datavalue at middle_value_key
        self.middle_sign = self.calculate_middle_sign(_dataset)
        # quad indices of quads connected to this edge with an edge
        self.manifold_edge_quads_ids = _manifold_edge_quad_ids
        # quad indices of quads connected to this edge with a vertex
        self.manifold_vertex_quad_ids = 2 * [None]
        self.manifold_vertex_quad_ids[0] = _manifold_vertex_quad_ids_dict[self.v_idx[0]]
        self.manifold_vertex_quad_ids[1] = _manifold_vertex_quad_ids_dict[self.v_idx[1]]

        # kind of the vertex. A vertex is either connected to the outside of the volume or to the inside (hybrid configurations and connections to other manifold edges are also possible!)
        self.v_kind = [None] * 2
        for local_v_idx in range(2):
            self.v_kind[local_v_idx] = self.determine_kind_of_vertex(local_v_idx, _dataset, _manifold_edge_set)

    def determine_kind_of_vertex(self, _local_v_idx, _dataset, _manifold_edge_set):

        # 1.    is the vertex connected to another manifold edge?
        #       check references by other manifold edges!
        other_manifold_edges = list(sorted(_manifold_edge_set))
        print other_manifold_edges
        print tuple(sorted(self.v_idx))
        other_manifold_edges.remove(tuple(sorted(self.v_idx)))
        other_manifold_edges = np.array(other_manifold_edges)

        if self.v_idx[_local_v_idx] in other_manifold_edges:
            return "manifold"

        # 2.    is the vertex connected to the outside or inside plane?
        #       go some further steps in manifold edge direction and evaluate data!
        if _local_v_idx == 0:
            edge_dir_value_key = tuple(np.array(self.middle_value_key) + self.resolution * self.edge_dir01)
        elif _local_v_idx == 1:
            edge_dir_value_key = tuple(np.array(self.middle_value_key) - self.resolution * self.edge_dir01)
        else:
            print "dc3D - determine_kind_of_vertex: UNDEFINED INDEX!"
            quit()

        edge_dir_perpendicular = 4 * [np.array([0,0,0])]
        idx = 0
        for d in range(3):
             if d != self.edge_dim:
                 for value in [-1,1]:
                    edge_dir_perpendicular[idx][d] = value
                    idx += 1

        perp_signs = 4 * [None] # check the four signs perpendicular to the edge direction
        for idx in range(4):
            edge_dir_perpendicular_key = tuple(np.array(edge_dir_value_key) + self.resolution * edge_dir_perpendicular[idx])
            if edge_dir_perpendicular_key in _dataset:
                perp_signs[idx] = _dataset[edge_dir_perpendicular_key] < 0
            else:
                perp_signs[idx] = False

        edge_dir_sign = None
        if edge_dir_value_key in _dataset:
            edge_dir_sign = _dataset[edge_dir_value_key] < 0
        else:
            edge_dir_sign = False

        if edge_dir_sign == False:
            return "outside" # (3.)
        else:
            return "inside" # (3.)

        return "hybrid" # (2.)

    def calculate_middle_sign(self, _dataset):
        key = self.middle_value_key
        if key in _dataset:
            return _dataset[key] > 0
        else:
            return False

    def calculate_edge_dir01(self):
        import numpy as np
        v_o = [None] * 2
        # v_o describes the origin of the respective voxel
        for i in range(2):
            v_o[i] = np.array(self.v_key[i])

        edge_dir01 = v_o[0] - v_o[1]
        edge_dir01 /= np.linalg.norm(edge_dir01)
        edge_dim = np.where(np.abs(edge_dir01) == 1)[0][0]

        return edge_dir01, edge_dim

    def calculate_middle_value_key(self):
        import numpy as np

        displacement = np.array([1.0, 1.0, 1.0]) * self.resolution / 2
        displacement[self.edge_dim] = 0.0
        if self.v_key[0][self.edge_dim] > self.v_key[1][self.edge_dim]:  # v_key[0] is in the plane crossed by the edge
            middle_plane_idx = 0
            return tuple(np.array(self.v_key[0]) + displacement), middle_plane_idx
        else:  # v_key[1] is in that plane
            middle_plane_idx = 1
            return tuple(np.array(self.v_key[1]) + displacement), middle_plane_idx

    def calculate_neighbour_keys(self):

        neighbor_directions = []

        for d in range(3):
            if d != self.edge_dim:
                for j in [-1, 1]:
                    neighbor_direction = np.zeros(3)
                    neighbor_direction[d] = j
                    neighbor_directions.append(neighbor_direction)

        neighbor_keys = 2 * [4 * [None]]
        for i in range(2):
            for j in range(4):
                neighbor_keys[i][j] = tuple(np.array(self.v_key[i]) + self.resolution * neighbor_directions[j])

        return neighbor_keys, neighbor_directions

    def resolve(self, _dataset, _vindex, _dc_quads, _dc_verts, o_idx_nodes):
        new_quads_list = [] # new quads contributed by this edge are stored here
        new_nodes = [] # new nodes introduced by manifold edge splitting are stored here
        delete_quads = self.manifold_edge_quads_ids  # the old quads connected to the manifold edge are deleted in any case!
        child_id = 0 # this will be incremented, after we have added an edge

        # we need to resolve the ambiguous cases: break or join surface with the new quads? Therefore we traverse all
        # the nodes in the same plane as the middle value
        for neighbour_pair_key in [(0, 2), (0, 3), (1, 2), (1, 3)]:  # create new quads and remove manifold quads
            # direction of the current node
            sign_direction = np.array(self.neighbour_directions[neighbour_pair_key[0]]) \
                             + np.array(self.neighbour_directions[neighbour_pair_key[1]])
            # key of the node
            sign_key = tuple(np.array(self.middle_value_key) + self.resolution * .5 * sign_direction)
            # value of the node
            sign = True
            if sign_key in _dataset:
                sign = _dataset[sign_key] > 0

            # resolves ambiguous case: if sign is equal to middle sign, we don't want to create a quad in between, which
            # separates the two nodes. If the signs are not equal, we want to separate them with two new quads
            if sign != self.middle_sign:
                new_quads = 2 * [None]  # init two quads

                # initialize new edge, the quads will be connected to instead of manifold edge
                normal_direction = sign_direction * self.resolution * 1.0/4.0  # the normal is in the direction of the sign
                for m_v_id in range(2):  # we will have to copy the manifold edge and shift it
                    new_nodes.append(_dc_verts[self.v_idx[m_v_id]]+normal_direction)  # shift new nodes into normal direction
                    self.v_children_idx[m_v_id][child_id] = o_idx_nodes+m_v_id # store global index of this node in object

                # each edge is parallel to the manifold edge, but shifted in the direction of one of the two neighbours
                for edge_id in range(2):
                    v_ids = 2 * [None] # find global neighbour vertex indices
                    for v_id in range(2):  # calculate ids of both vertices of the neighbouring edge
                        v_key = tuple(np.array(self.v_key[v_id])
                                           + self.resolution * self.neighbour_directions[neighbour_pair_key[edge_id]])
                        v_ids[v_id] = _vindex[v_key]

                    # calculate corresponding edge key
                    manifold_edge_key = tuple(sorted(tuple(v_ids)))

                    # find quad which contains this edge
                    for local_q_id in range(4):
                        quad = _dc_quads[self.manifold_edge_quads_ids[local_q_id]]

                        if quad_has_edge(quad, manifold_edge_key):
                            new_quads[edge_id] = list(quad) # copy quad

                            # swap both references to manifold edge with reference to newly created node
                            for m_v_id in range(2):
                                tmp = new_quads[edge_id].index(self.v_idx[m_v_id]) # find reference to node of manifold edge
                                new_quads[edge_id][tmp] = self.v_children_idx[m_v_id][child_id] # replace with reference to new node
                                for shift in [-1,+1]:
                                    neighbour_idx = quad[(tmp+shift)%4]
                                    if neighbour_idx != self.v_idx[int(not(m_v_id))]:
                                        self.v_children_connection_idx[m_v_id][child_id].add(neighbour_idx)

                            # only one quad out of self.manifold_edge_quads is connected to this neighbouring edge
                            continue

                o_idx_nodes += 2  # two new nodes have been introduces for the new edge, increment origin
                new_quads_list += new_quads  # append 2 new quads to new_quads_list
                child_id += 1  # incrementing child id


                #############################################
                # child of original manifold edge processes #
                #############################################

        ##########################
        # all children processed #
        ##########################

        # change remaining references to removed edge -> treat vertices!
        # this depends on the self.v_kind of the vertex!
        #       - If an outside vertex is removed, we will introduce a hexaedral face
        #       - If an inside vertex is removed, we will introduce two triangle faces
        # todo changing those non-quad shapes into quads again is a postprocessing step!

        return new_quads_list, new_nodes, delete_quads, o_idx_nodes

    def resolve_outside_vertex(self, _local_v_id, _dc_quads):
        # all quads connected to the vertex will be removed anyhow
        delete_quads = self.manifold_vertex_quad_ids[self.v_idx[_local_v_id]]
        new_quad = []
        # create a hexagon for outside vertices
        for q_idx in delete_quads:
            quad = _dc_quads[q_idx]
            end_idx = np.where(np.array(quad) == self.v_idx[_local_v_id])[0][0]
            start_idx = (end_idx + 1) % 4

            if end_idx == 0:
                new_quad_part = quad[start_idx:]
            elif start_idx > end_idx:
                new_quad_part = np.concatenate([quad[start_idx:], quad[:end_idx]], 0)
            else:
                new_quad_part = quad[start_idx:end_idx]

            new_quad = np.concatenate([new_quad, new_quad_part], 0)

        return [new_quad.tolist()], delete_quads

    def resolve_inside_vertex(self, _local_v_id, _dc_quads):
        # all quads connected to the vertex will be removed anyhow
        delete_quads = list(self.manifold_vertex_quad_ids[self.v_idx[_local_v_id]])
        new_quad = []

        # do any of the quads connected to the vertex have a common edge?

        # build edge usage list
        edge_usage_list = {}
        for local_q_id in range(delete_quads.__len__()):
            global_q_id = delete_quads[local_q_id]
            q = _dc_quads[global_q_id]
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
                    edge_usage_list[e].append(local_q_id)  # append current quad id, since quad is using this edge
                else:
                    edge_usage_list[e] = [local_q_id]  # add key to list and save quad id, since quad is using this edge

        # common and not common edge quads are saved here with respect to their local id in the delete_quads list.
        common_edge_list = {}
        no_common_edge_list = range(delete_quads.__len__())

        #searching common edges
        for edge, q_edge in edge_usage_list.items():
            if q_edge.__len__() > 1: # this is a common edge!
                common_edge_list[tuple(q_edge)] = list(edge)
                for local_q_id in q_edge:
                    no_common_edge_list.remove(local_q_id)

        # #generating pentagons
        # for q_local_idx_pair, common_edge in common_edge_list.items():  # if common edge: remove manifold vertex from both and combine them into a pentagon
        #     pent = []
        #
        #     q_idx = 2 * [None]
        #     q = 2 * [None]
        #     start_q = 2 * [None]
        #     end_q = 2 * [None]
        #
        #     v_global_idx = self.v_idx[_local_v_id]
        #     for i in range(2):
        #         q_idx[i] = delete_quads[q_local_idx_pair[i]]
        #         q[i] = _dc_quads[q_idx[i]]
        #         start_q[i] = (q[i].index(v_global_idx) + 1) % 4
        #         end_q[i] = q[i].index(v_global_idx)
        #         if start_q[i] < end_q[i]:
        #             pent += q[i][start_q[i]:end_q[i]]
        #         else:
        #             pent += q[i][start_q[i]:] + q[i][:end_q[i]]
        #
        #     not_v_edge_index = int(not(common_edge.index(v_global_idx)))
        #     pent.remove(common_edge[not_v_edge_index])
        #     new_quad.append(pent)
        #
        #     new_quad.append(q[0])
        #     new_quad.append(q[1])

        # generating triangles for common edges
        for q_local_idx_pair, common_edge in common_edge_list.items():
            v_global_idx = self.v_idx[_local_v_id]
            tri = [v_global_idx]

            q_idx = 2 * [None]
            q = 2 * [None]

            for i in range(2):
                q_idx[i] = delete_quads[q_local_idx_pair[i]]
                q[i] = _dc_quads[q_idx[i]]
                v_quad_idx = q[i].index(v_global_idx)
                if q[i][(v_quad_idx + 1)%4] in common_edge:
                    tri.append(q[i][(v_quad_idx - 1)%4])
                else:
                    tri.append(q[i][(v_quad_idx + 1)%4])

                new_quad.append(q[i])

            new_quad.append(tri)

        # generating triangles for non common edges
        for q_local_idx in no_common_edge_list:  # if no common edge: just remove the manifold vertex and create a triangle
            q = delete_quads[q_local_idx]
            tri = _dc_quads[q]
            tri.remove(self.v_idx[_local_v_id])
            new_quad.append(tri)

        return new_quad, delete_quads

    def resolve_manifold_vertex(self, _local_v_id, _dc_quads):
        # all quads connected to the vertex will be removed anyhow
        delete_quads = list(self.manifold_vertex_quad_ids[self.v_idx[_local_v_id]])
        # no new quads are generated!
        new_quad = []

        return new_quad, delete_quads


# searches the corresponding key with a given vertex index
def search_vertex_key_from_index(_dc_vindex, idx):
    for key in _dc_vindex:
        if int(_dc_vindex[key]) == int(idx):
            return key

    print "ERROR! INDEX %d not found" % idx
    quit()
