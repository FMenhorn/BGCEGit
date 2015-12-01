__author__ = 'erik'


class Edge:
    def __init__(self, _id, _vertex1, _vertex2):

        self.id = _id
        self.vertices = [_vertex1, _vertex2]
        for vertex in self.vertices:
            vertex.add_edge(self)

        self.quads = []

    def add_quad(self, quad):
        self.quads.append(quad)

    def get_vertices(self):
        return self.vertices

    def get_quads(self):
        return self.quads
