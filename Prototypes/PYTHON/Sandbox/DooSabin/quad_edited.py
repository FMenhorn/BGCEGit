__author__ = 'benjamin, anna'
import numpy as np

class Face:
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _id, _vertices):


        self.quad_id = _id
        self.vertices = _vertices
        self.centroid = self.compute_centroid(_vertices)
        self.vertex_ids = np.array([self.vertices[i].getId() for i in range(len(self.vertices))])

    def getEdges(self):

        edges = np.array([])
        n = len(self.vertices)

        for i in range(n):
            np.append(edges, [self.vertices[i], self.vertices[(i+1)%n]])

        return edges

    def find_neighbors(self, facelist):

        neighbors = np.array([])

        edges = self.getEdges()

        for face in facelist:
            face_edges_ids = face.getEdges()


        for e in edges:
            has_vertex1 = np.where([quadlist[i].vertex_ids for i in range(len(quadlist))] == e[0])[0]
            has_vertex2 = np.where([quadlist[i].vertex_ids for i in range(len(quadlist))] == e[1])[0]
            same_edge = np.intersect1d(has_vertex1, has_vertex2)
            neighbor = same_edge[same_edge != self.quad_id]
            neighbors = np.append(neighbors, neighbor)

        return neighbors.astype(int)

    def listOfFacesContainingTheEdge(self, quadlist, edge):
        return