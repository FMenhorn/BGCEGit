__author__ = 'benjamin'

import numpy as np
from Vertex import Vertex2


class VertexDC2(Vertex2):
    def __init__(self, _id, _x, _y):
        super(VertexDC2, self).__init__(_id, _x, _y)
        self.linked_to_voxel = []

    def link_to_voxel(self, _voxel):
        self.linked_to_voxel.append(_voxel)

v1 = VertexDC2(0,1.0,1.2)