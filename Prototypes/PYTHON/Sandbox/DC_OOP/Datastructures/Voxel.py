import numpy as np

__author__ = 'benjamin'

from BasicDatastructures import Point

# Vertices of quad
voxel2_verts = [np.array([0.0, 0.0]),
                np.array([1.0, 0.0]),
                np.array([1.0, 1.0]),
                np.array([0.0, 1.0])] # traverse verts  of voxel in CCW manner

def Voxel2(object):
    def __init__(self, _origin, _size, _datapoints):
        self.origin = Point(_origin)
        self.size = _size
        self.datapoints = self.store_in_local_coordinates(_datapoints)

    def store_in_local_coordinates(_datapoints):


    def get_signs(self):
        return [False, False, False, False]


