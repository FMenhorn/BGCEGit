import matplotlib.pyplot as plt

__author__ = 'erik'

class Edge(object):
    _counter_id = 0

    def __init__(self, _vertex1, _vertex2):
        self._id = self._counter_id
        self._counter_id += 1
        self._vertices = [_vertex1, _vertex2]
        for vertex in self._vertices:
            vertex.add_edge(self)

    def get_vertices(self):
        return self._vertices

    def get_id(self):
        return self._id


class Edge3(Edge):


    def __init__(self, _vertex1, _vertex2):
        super(Edge3, self).__init__(_vertex1, _vertex2)
        self.quads = []

    def add_quad(self, quad):
        self.quads.append(quad)

    def get_quads(self):
        return self.quads


class Edge2(Edge):
    def __init__(self, _vertex1, _vertex2):
        super(Edge2, self).__init__(_vertex1, _vertex2)

    def draw(self):
        p0 = self._vertices[0].get_position()
        p1 = self._vertices[1].get_position()
        x = [p0[0], p1[0]]
        y = [p0[1], p1[1]]
        plt.plot(x,y,'k-')

class Edge2DC(Edge2):
    def __init__(self):
        super(Edge2, self).__init__(None, None)

    def connect_to_vertex(self, vtx):
        if self._vertices[0] == None:
            self._vertices[0] = vtx
        elif self._vertices[1] == None:
            self._vertices[1] = vtx
        else:
            raise Exception("Edge already has two vertices!")
