from Point import Point
import matplotlib.pyplot as plt

__author__ = 'erik'


class AbstractVertex(Point):
    _id_counter = 0

    def __init__(self, pos):
        super(AbstractVertex, self).__init__(pos)
        self._id = self._obtain_id()
        self._edges = []

    def add_edge(self, edge):
        self._edges.append(edge)

    def get_edges(self):
        return self._edges

    def _obtain_id(self):
        id = AbstractVertex._id_counter
        AbstractVertex._id_counter += 1
        return id

class Vertex2(AbstractVertex):
    def __init__(self, x, y):
        super(Vertex2, self).__init__([float(x),float(y)])

    def draw(self):
        p = self.get_position()
        plt.plot(p[0],p[1],'ko')


class Vertex3(AbstractVertex):
    def __init__(self, x, y, z):
        super(Vertex3, self).__init__([float(x),float(y),float(z)])
        self._quads = []

    def add_quad(self, quad):
        self._quads.append(quad)

    def get_quads(self):
        return self._quads


class AbstractVertexDC(object):
    def _link_to_edges(self, connectivity):
        for voxel_edge in connectivity:
            voxel_edge.link_to(self)


class VertexDC2(Vertex2, AbstractVertexDC):
    def __init__(self, x, y, connectivity):
        super(VertexDC2, self).__init__(x, y)
        self._link_to_edges(connectivity)


class VertexDC3(Vertex3, AbstractVertexDC):
    def __init__(self, x, y, z, connectivity):
        super(VertexDC3, self).__init__(x, y, z)
        self._link_to_edges(connectivity)

