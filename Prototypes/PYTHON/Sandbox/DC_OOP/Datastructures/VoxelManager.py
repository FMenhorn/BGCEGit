__author__ = 'benjamin'

import itertools as it

import numpy as np

from Voxel import Voxel2, Voxel3
from Edge import Edge2


class AbstractVoxelManager(object):
    def __init__(self, resolution, min_data, max_data, dataset):
        self._voxel_dict = {}
        self._resolution = float(resolution)
        self._min_origin = float(min_data)
        self._max_origin = float(max_data)
        self._num_voxels = ((self._max_origin - self._min_origin) / self._resolution)**self._dimension
        self._setup_voxel_dict(dataset)

    def get_voxel_dict(self):
        return self._voxel_dict

    def get_voxel_vertices(self):
        voxel_vertices = []
        for key, voxel in self._voxel_dict.items():
            dc_vertices = voxel.get_dc_vertices()
            if dc_vertices.__len__() > 0:
                voxel_vertices.append(dc_vertices)
        return voxel_vertices

    def calculate_dc_vertices(self):
        for key, voxel in self._voxel_dict.items():
            voxel.generate_dc_vertices()

    def draw_voxels(self):
        for origin, voxel in self._voxel_dict.items():
            voxel.draw()


class VoxelManager2(AbstractVoxelManager):
    _dimension = 2

    def __init__(self, resolution, min_data, max_data, dataset):
        super(VoxelManager2, self).__init__(resolution, min_data, max_data, dataset)

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

    def get_voxel_edges(self):
        return Voxel2._voxel_edge_manager.create_all_dc_edges()


class VoxelManager3(AbstractVoxelManager):
    _dimension = 3
    _ax = None

    def __init__(self, resolution, min_data, max_data, dataset):
        super(VoxelManager3,self).__init__(resolution, min_data, max_data, dataset)

    def _setup_voxel_dict(self, dataset):

        for x, y, z in it.product(np.arange(self._min_origin, self._max_origin, self._resolution),
                                  np.arange(self._min_origin, self._max_origin, self._resolution),
                                  np.arange(self._min_origin, self._max_origin, self._resolution)):
            key = (x, y, z)
            origin = np.array([x, y, z])
            self._voxel_dict[key] = Voxel3(origin, self._resolution, dataset)

    def set_ax(self, ax):
        VoxelManager3._ax = ax
        for key, vox in self._voxel_dict.items():
            print type(vox)
            vox.set_ax(ax)


