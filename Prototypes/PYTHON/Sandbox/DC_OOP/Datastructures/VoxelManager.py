__author__ = 'benjamin'

import itertools as it

import numpy as np

from Voxel import Voxel2, Voxel3


class AbstractVoxelManager(object):
    _dimension = None
    _voxel_dict = {}
    _resolution = None
    _min_origin = None
    _max_origin = None
    _num_voxels = None

    def __init__(self, resolution, min_data, max_data):
        self._resolution = float(resolution)
        self._min_origin = float(min_data)
        self._max_origin = float(max_data)
        self._num_voxels = ((self._max_origin - self._min_origin) / self._resolution)**self._dimension


class VoxelManager2(AbstractVoxelManager):
    _dimension = 2

    def __init__(self, resolution, min_data, max_data, dataset):
        super(VoxelManager2, self).__init__(resolution, min_data, max_data)
        self._setup_voxel_dict(dataset)

    def _setup_voxel_dict(self, dataset):
        for x, y in it.product(np.arange(self._min_origin,
                                         self._max_origin,
                                         self._resolution),
                               np.arange(self._min_origin,
                                         self._max_origin,
                                         self._resolution)):
            key = (x, y)
            origin = np.array([x, y])
            self._voxel_dict[key] = Voxel2(origin, self._resolution, dataset)


class VoxelManager3(AbstractVoxelManager):
    _dimension = 3

    def __init__(self, resolution, min_data, max_data, dataset):
        super(VoxelManager3,self).__init__(resolution, min_data, max_data)
        self._setup_voxel_dict(dataset)

    def _setup_voxel_dict(self, dataset):

        for x, y, z in it.product(np.arange(self._min_origin, self._max_origin, self._resolution),
                                  np.arange(self._min_origin, self._max_origin, self._resolution),
                                  np.arange(self._min_origin, self._max_origin, self._resolution)):
            key = (x, y, z)
            origin = np.array([x, y, z])
            self._voxel_dict[key] = Voxel3(origin, self._resolution, dataset)

