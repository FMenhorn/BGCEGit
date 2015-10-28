import numpy as np

__author__ = 'benjamin'


class ManifoldNode:
    def __init__(self, _voxel_coord, _quad_sign_keys, _dataset, _resolution):
        self.voxel_coord = _voxel_coord
        self.res = _resolution
        self.x = _voxel_coord[0] + .5*self.res
        self.y = _voxel_coord[1] + .5*self.res
        self.middle_key = tuple(np.array([self.x, self.y]))
        self.middle_sign = _dataset[self.middle_key] > 0
        self.quad_sign_keys = _quad_sign_keys
        self.quad_signs = self.calculate_quad_signs(_dataset)
        self.connects, self.normal = self.calculate_connection()

    def calculate_quad_signs(self, _dataset):
        quad_signs = []

        for key in self.quad_sign_keys:
            c = True
            if key in _dataset:
                c = _dataset[key] > 0
            quad_signs.append(c)

        return quad_signs

    def calculate_connection(self):
        connects = [] # list holding connectivity for first and second resolved ManifoldNode
        normals = [] # list holding normal on first and second edge passing the respective resolved ManifoldNode
        neighbor_keys = [tuple(self.voxel_coord + self.res * np.array([-1.0,0.0])),
                         tuple(self.voxel_coord + self.res * np.array([0.0,-1.0])),
                         tuple(self.voxel_coord + self.res * np.array([1.0,0.0])),
                         tuple(self.voxel_coord + self.res * np.array([0.0,1.0]))]

        n = self.quad_signs.__len__()
        for i in range(n):
            if self.middle_sign != self.quad_signs[i]: # calculate normal and add edge dividing inside and outside
                connects.append((neighbor_keys[i],neighbor_keys[(i+1)%n])) # add edge
                normal = (np.array(self.quad_sign_keys[i]) - np.array(self.middle_key))*3.0/4.0
                normals.append(normal)

        return connects, normals

    def resolve(self, o_idx_nodes, global_idx, vindex, node_usage_list):
        new_nodes = []  # is list of vertices which will be appended
        new_edges = []  # is list of edges (two node ids) which will be appended

        for i in range(2): # loop over all resolved manifold nodes
            new_node = (np.array([self.x,self.y])+self.normal[i]).tolist()  # new resolved manifold node i
            new_nodes.append(new_node)  # at position o_idx_nodes

            new_edge = 2*[None]
            for j in range(2):  # loop over all neighbours of resolved manifold node
                # connect j-th neighbour of resolved manifold node i with this node
                new_edge[j] = [o_idx_nodes, vindex[self.connects[i][j]]]

            o_idx_nodes += 1
            new_edges += new_edge  # add new edges

        delete_edges = node_usage_list[global_idx]  # is list of edges, using this node, which will be deleted

        return new_edges, new_nodes, delete_edges, o_idx_nodes
