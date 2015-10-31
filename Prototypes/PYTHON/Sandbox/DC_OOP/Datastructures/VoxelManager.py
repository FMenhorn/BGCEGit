__author__ = 'benjamin'

import itertools as it

import numpy as np

from Voxel import Voxel2, Voxel3


class AbstractVoxelManager(object):
    def __init__(self, resolution, min_data, max_data):
        self._voxel_dict = {}
        self._resolution = float(resolution)
        self._min_origin = float(min_data)
        self._max_origin = float(max_data)
        self._num_voxels = ((self._max_origin - self._min_origin) / self._resolution)**self._dimension

    def get_voxel_dict(self):
        return self._voxel_dict

    def get_voxel_vertices(self):
        voxel_vertices = {}
        for origin, voxel in self._voxel_dict.items():
            dc_vertices = voxel.get_dc_vertices()
            if dc_vertices.__len__() > 0:
                voxel_vertices[origin] = dc_vertices
        return voxel_vertices

    def calculate_dc_vertices(self):
        for origin, voxel in self._voxel_dict.items():
            connectivity = voxel.generate_dc_vertices()

    def draw_voxels(self):
        for origin, voxel in self._voxel_dict.items():
            voxel.draw_voxel()


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

    def set_ax(self, ax):
        self._ax = ax
        for key, vox in self._voxel_dict.items():
            print type(vox)
            vox.set_ax(ax)


