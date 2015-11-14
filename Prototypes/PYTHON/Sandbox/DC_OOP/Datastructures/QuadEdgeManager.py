from Edge import Edge3

__author__ = 'benjamin'


class QuadEdgeManager:
    def __init__(self):
        self._edgedict = {}

    def get_quad_edge(self, vertices):
        key = tuple({vertices[0], vertices[1]})
        id_key = tuple(sorted([key[0].get_id(),key[1].get_id()]))
        if id_key in self._edgedict: # edge already in manager
            return self._edgedict[id_key]
        else: # create new edge in manager
            new_edge = self._create_quad_edge(vertices)
            self._edgedict[id_key] = new_edge
            return new_edge

    def _create_quad_edge(self, vertices):
        return Edge3(vertices[0], vertices[1])
