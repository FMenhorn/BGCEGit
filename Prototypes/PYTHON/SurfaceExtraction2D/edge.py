__author__ = 'benjamin'


class Edge:
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _id, _edgelist, _vertexlist):
        import numpy as np
        if not (type(_edgelist) is np.ndarray and type(_vertexlist) is np.ndarray):
            print "WRONG TYPE! exiting..."
            quit()

        self.edge_id = _id
        self.vertex_ids = _edgelist[_id]
        self.vertices_edge = _vertexlist[self.vertex_ids]
        self.centroid = self.compute_centroid(_vertexlist)
        self.normal = self.compute_normal(_vertexlist)
        self.ortho_basis_AB, self.basis_AB = self.compute_basis(_vertexlist)# [edge_AB;normal]

        self.neighbors = self.find_neighbors(_edgelist)
        #self.basis, self.basis_inv = self.get_basis()

    def compute_centroid(self, _vertexlist):
        import numpy as np
        return np.mean(_vertexlist[self.vertex_ids],0)

    def compute_normal(self, _vertexlist):
        import numpy as np

        vertex1 = _vertexlist[self.vertex_ids[0]]
        vertex2 = _vertexlist[self.vertex_ids[1]]

        edge12 = vertex2-vertex1

        normal = np.array([-edge12[1],edge12[0]])
        normal /= np.linalg.norm(normal)

        return normal

    def compute_basis(self, _vertexlist):
        import numpy as np

        vertexA = self.vertices_edge[0,:]
        vertexB = self.vertices_edge[1,:]
        edgeAB = vertexB - vertexA
        edgeAB_normalized = edgeAB / np.linalg.norm(edgeAB)

        ortho_basis_AB = np.array([self.normal,
                                   edgeAB_normalized])

        basis_AB = np.array([self.normal,
                             edgeAB])

        return ortho_basis_AB.transpose(), basis_AB.transpose()

    def projection_onto_line(self, _point):
        import numpy as np

        distance = np.dot(self.centroid-_point, self.normal)
        projected_point = _point+distance*self.normal
        return projected_point, distance

    def point_on_edge(self, t):
        import numpy as np

        if t > 1 or t < 0:
            print "INVALID INPUT!"
            quit()
        else:
            vertexA = self.vertices_edge[0,:]
            point = vertexA + np.dot(self.basis_AB[:,1],t)

        return point

    def projection_onto_edge(self, _point):
        from scipy.linalg import solve_triangular
        import numpy as np

        vertexA = self.vertices_edge[0,:]
        vector_vertexA_point = _point - vertexA
        # we want to transform _point to the BASIS=[normal,AB] and use QR decomposition of BASIS = Q*R
        # BASIS * coords = _point -> R * coords = Q' * _point
        R_AB = np.dot(self.ortho_basis_AB.transpose(),self.basis_AB)
        b = np.dot(self.ortho_basis_AB.transpose(),vector_vertexA_point)
        x = solve_triangular(R_AB,b)
        distance = x[0]
        projected_point = _point - distance * self.normal
        t = x[1]

        distance = abs(distance)

        if t < 0:
            t = 0
        elif t > 1:
            t = 1

        projected_point = self.point_on_edge(t)
        distance = np.linalg.norm(_point-projected_point)

        return projected_point, distance, t

    def measure_centroid_distance_squared(self, _point):
        import numpy as np

        r = self.centroid-_point
        return np.dot(r,r)

    def find_neighbors(self,_edgelist):
        import numpy as np

        neighbors = np.array([])

        for v in self.vertex_ids:
            same_vertex = np.where(_edgelist == v)[0]
            neighbor = same_vertex[same_vertex != self.edge_id]
            neighbors = np.append(neighbors, neighbor)

        return neighbors.astype(int)