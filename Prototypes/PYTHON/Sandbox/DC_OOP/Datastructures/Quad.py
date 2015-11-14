__author__ = 'erik'


class Quad:

    _id_counter = 0

    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _vertex1, _vertex2, _vertex3, _vertex4, _edge1, _edge2, _edge3, _edge4):

        self.id = self._obtain_id()
        self.vertices = [_vertex1, _vertex2, _vertex3, _vertex4]
        for vertex in self.vertices:
            vertex.add_quad(self)

        self.edges = [_edge1, _edge2, _edge3, _edge4]
        for edge in self.edges:
            edge.add_quad(self)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_opposite_vertex(self, vertex):
        vertex_index = self.vertices.index(vertex)
        opposite_index = (vertex_index + 2) % 4
        return self.vertices[opposite_index]

    def get_edge_neighbouring_quads(self):
        quad_list = []
        for edge in self.edges:
            for quad in edge.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return quad_list

    def get_vertex_neighbouring_quads(self):
        quad_list = []
        for vertex in self.vertices:
            for quad in vertex.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return quad_list

    def _obtain_id(self):
        id = Quad._id_counter
        Quad._id_counter += 1
        return id

    # def replace_edge(self, old_edge, new_edge):
    #     edge_index = self.edges.index(old_edge)
    #     edge_vertices = self.edges[edge_index].get_vertices
    #
    #     self.vertices[self.vertices.index(edge_vertices[0])] = new_edge.get_vertices[0]
    #     self.vertices[self.vertices.index(edge_vertices[1])] = new_edge.get_vertices[1]
    #
    # def replace_vertex(self, old_vertex, new_vertex):
    #     vertex_index = self.vertices.index(old_vertex)
    #
    #     old_vertex.get_edges
