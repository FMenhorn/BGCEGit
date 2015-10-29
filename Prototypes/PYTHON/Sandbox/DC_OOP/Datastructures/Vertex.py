from BasicDatastructures import Point

__author__ = 'erik'


class Vertex3(Point):
    def __init__(self, id, x, y, z):

        super(Vertex3, self).__init__([float(x),float(y),float(z)])
        self._id = id
        self._edges = []
        self._quads = []

    def add_edge(self, edge):
        self._edges.append(edge)

    def add_quad(self, quad):
        self._quads.append(quad)

    def get_edges(self):
        return self._edges

    def get_quads(self):
        return self._quads


class Vertex2(Point):
    def __init__(self, id, x, y):

        super(Vertex2, self).__init__([float(x),float(y)])
        self._id = id
        self._edges = []

    def add_edge(self, edge):
        self._edges.append(edge)

    def get_edges(self):
        return self._edges
