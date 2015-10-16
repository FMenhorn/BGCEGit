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

        neighbors = []

        edges = self.getEdges()

        for face in facelist:

            if face.id <> self.quad_id:

                face_edges = face.getEdges()

                for edge in face_edges:
                    if (edge in edges):
                        neighbors.append(face)

        return neighbors
