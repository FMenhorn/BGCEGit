__author__ = 'erik + jc + anna'
class Shape(object):
    def __init__(self, id, vertices):
        self._id = id
        self._vertices = vertices

    def get_vertices(self):
        return self._vertices

class Quad(Shape):
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, id, vertex1, vertex2, vertex3, vertex4, edge1, edge2, edge3, edge4):

        super(Quad, self).__init__(id, [vertex1, vertex2, vertex3, vertex4])
        #self._id = id
       # self._vertices = [vertex1, vertex2, vertex3, vertex4]
        for vertex in self._vertices:
            vertex.add_quad(self)

        self._edges = [edge1, edge2, edge3, edge4]
        for edge in self._edges:
            edge.add_quad(self)

    def get_vertices(self):
        return self._vertices

    def get_edges(self):
        return self._edges

    def get_opposite_vertex(self, vertex):
        vertex_index = self._vertices.index(vertex)
        opposite_index = (vertex_index + 2) % 4
        return self._vertices[opposite_index]

    def get_edge_neighbouring_quads(self):
        quad_list = []
        for edge in self._edges:
            for quad in edge.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return quad_list

    def get_vertex_neighbouring_quads(self):
        quad_list = []
        for vertex in self._vertices:
            for quad in vertex.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return
