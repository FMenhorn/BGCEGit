__author__ = 'benjamin'

from Vertex import Vertex2


class VertexDC2(Vertex2):
    def __init__(self, id, x, y):
        super(VertexDC2, self).__init__(id, x, y)
        self.linked_to_voxel = []

    def link_to_voxel(self, _voxel):
        self.linked_to_voxel.append(_voxel)

v1 = VertexDC2(0,1.0,1.2)