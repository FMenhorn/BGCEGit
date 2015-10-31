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

class VertexDC2(Vertex2):
    def __init__(self, id, x, y):
        super(VertexDC2, self).__init__(id, x, y)
        self._connected_to = []

    def connect_to_voxel(self, voxel):
        self._connected_to.append(voxel)


class VertexDC3(Vertex3):
    def __init__(self, id, x, y, z):
        super(VertexDC3, self).__init__(id, x, y, z)
        self._connected_to = []

    def connect_to_voxel(self, voxel):
        self._connected_to.append(voxel)

