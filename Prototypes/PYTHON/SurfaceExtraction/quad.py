__author__ = 'benjamin'


class Quad:
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _id, _quadlist, _vertexlist):
        import numpy as np
        if not (type(_quadlist) is np.ndarray and type(_vertexlist) is np.ndarray):
            print "WRONG TYPE! exiting..."
            quit()

        self.id = _id
        self.vertices = _quadlist[_id]
        self.centroid = self.compute_centroid(_vertexlist)
        self.plane = self.compute_plane(_vertexlist)
        self.normal = self.compute_normal(_vertexlist)
        self.neighbors = self.find_neighbors(_quadlist)

    def compute_centroid(self, _vertexlist):
        import numpy as np
        return np.mean(_vertexlist[self.vertices],0)

    def compute_plane(self, _vertexlist):
        import numpy as np

        A=_vertexlist[self.vertices[0]]
        B=_vertexlist[self.vertices[1]]
        C=_vertexlist[self.vertices[2]]
        D=_vertexlist[self.vertices[3]]

        AB=B-A
        AC=C-A
        AD=D-A

        Q=np.array([AB,AC,AD])

        return abs(np.linalg.det(Q))<10**-14

    def compute_normal(self, _vertexlist):
        import numpy as np

        if self.plane:
            vertex1 = _vertexlist[self.vertices[1]]
            vertex2 = _vertexlist[self.vertices[2]]
            vertex3 = _vertexlist[self.vertices[3]]

            edge12 = vertex2-vertex1
            edge13 = vertex3-vertex1

            normal = np.cross(edge12,edge13)
            normal /= np.linalg.norm(normal)

        else:
            #find least squares fit plane
            lsq_matrix = _vertexlist[self.vertices] - self.centroid
            u, s, v = np.linalg.svd(lsq_matrix)
            idx = np.where(np.min(abs(s)) == abs(s))[0][0]

            normal = v[idx, :]
            normal /= np.linalg.norm(normal)

        return normal

    def compute_corner_points(self, _vertexlist):
        import numpy as np

        if self.plane:
            return _vertexlist[self.vertices]
        else:
            #return corner points projected onto fit plane!
            lsq_matrix = _vertexlist[self.vertices] - self.centroid
            distance = np.dot(lsq_matrix, self.normal)
            return _vertexlist[self.vertices]-np.outer(distance,self.normal)

    def find_neighbors(self,_quadlist):
        import numpy as np

        neighbors = np.array([])

        edges = [self.vertices[[0,1]],
                 self.vertices[[1,2]],
                 self.vertices[[2,3]],
                 self.vertices[[3,0]]]

        for e in edges:
            has_vertex1 = np.where(_quadlist == e[0])[0]
            has_vertex2 = np.where(_quadlist == e[1])[0]
            same_edge = np.intersect1d(has_vertex1, has_vertex2)
            neighbor = same_edge[same_edge != self.id]
            neighbors = np.append(neighbors, neighbor)

        return neighbors.astype(int)

