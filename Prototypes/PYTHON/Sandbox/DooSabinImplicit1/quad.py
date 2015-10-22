import numpy as np
__author__ = 'benjamin'


class Quad:
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _id, _vertices):

        self.quad_id = _id
        self.matlab_id = _id+1
        self.vertices = _vertices
        self.vertex_ids = np.array([self.vertices[i].getId() for i in range(len(self.vertices))])
        self.centroid = self.compute_centroid()
        #types can be: vertex, edge, center
        self.type = ""
        self.parent_type = ""
        self.parents = []
        #only for the faces which were generated from some vertex children
        self.parent_vertex = None
        self.edges = self.getEdges()
        self.parent_edge = None
        self.dooSabinVertices = [None]*16


       # self.neighbors = self.find_neighbors(_quadlist)
        #self.basis, self.basis_inv = self.get_basis()

    def compute_centroid(self):
        return np.mean([self.vertices[i].coordinates for i in range(len(self.vertices))], 0)

    def getEdges(self):

        edges = []
        n = len(self.vertices)

        for i in range(n):
            edges.append([self.vertices[i], self.vertices[(i+1)%n]])

        return edges

    def isAdjacent(self, face):
        face_edges = face.getEdges();
        flag = 0
        shared_edge = None
        for edge in self.getEdges():
            if (edge in face_edges) or ([edge[1], edge[0]] in face_edges):
                #flag = 1
                shared_edge = edge

        return shared_edge

    def adjacentEdges(self, vert):
        adjacent_edges = []
        for edge in self.getEdges():
            if vert in edge:
                adjacent_edges.append(edge)
        return adjacent_edges


   # def find_neighbors(self, facelist):
#
 #       neighbors = []
#
 #       edges = self.getEdges()

#        for face in facelist:
#
 #           if face.quad_id != self.quad_id:

  #              face_edges = face.getEdges()

   #             for edge in face_edges:
    #                if (edge in edges):
     #                   neighbors.append(face)

#        return neighbors