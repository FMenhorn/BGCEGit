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
        self._setup_voxel_neighbors()

    def get_voxel_dict(self):
        return self._voxel_dict

    def get_voxel_vertices(self):
        voxel_vertices = {}
        for key, voxel in self._voxel_dict.items():
            dc_vertices = voxel.get_dc_vertices()
            if dc_vertices.__len__() > 0:
                voxel_vertices[key] = dc_vertices
        return voxel_vertices

    def calculate_dc_vertices(self):
        for key, voxel in self._voxel_dict.items():
            voxel.generate_dc_vertices()

    def calculate_connections(self):
        self.edge_list = []
        print "\n\n###DRAWING CONNECTIONS!###"
        for key, voxel in self._voxel_dict.items(): # traverse all voxels
            print "\tVOXEL: "+str(voxel)+ "@"+str(voxel.get_origin())
            for vertex in voxel.get_dc_vertices(): # for each voxel traverse the vertices in this voxel
                print "has \tVERTEX: "+str(vertex)+ "@" + str(vertex.get_position())
                connectivity = vertex.linked_to_voxel # get connectivity of the vertex
                for connected_voxels in connectivity: # traverse the connected voxelsets
                    print "with \tCONNECTION: "+str(connected_voxels)
                    for connected_voxel in connected_voxels: # traverse all voxels of the current set
                        print "#OTHER"
                        print "\tVOXEL: "+str(connected_voxel)+ "@"+str(connected_voxel.get_origin())
                        for connected_vertex in connected_voxel.get_dc_vertices(): # traverse all vertices in the connected voxel
                            print "has \tVERTEX: "+str(connected_vertex)+ "@" + str(connected_vertex.get_position())
                            other_connectivity = connected_vertex.linked_to_voxel
                            for other_voxels in other_connectivity: # traverse voxelsets this vertex is connected to
                                print "with \tCONNECTION: "+str(other_voxels)
                                for other_voxel in other_voxels: # traverse all voxels of the other set
                                    print "one \tVOXEL: "+str(other_voxel)+"@"+str(other_voxel.get_origin())
                                    if other_voxel == voxel: # found this voxel in connectivity list
                                        print "FOUND CONNECTION!"
                                        #remove it from both connectivity lists and create edge
                                        print "vertex "+str(vertex)+" from voxel "+str(voxel)+" connected to "+str(connected_voxel)
                                        print "VICE VERSA"
                                        print "vertex "+str(connected_vertex)+" from voxel "+str(connected_voxel)+" connected to "+str(voxel)
                                        print "##############"
                                        print connected_voxels
                                        print connected_voxel
                                        connected_voxels.remove(connected_voxel)
                                        other_voxels.remove(other_voxel)
                                        self.edge_list.append(Edge2(vertex, connected_vertex))

    def draw_voxels(self):
        for origin, voxel in self._voxel_dict.items():
            voxel.draw_voxel()

    def draw_edges(self):
        for edge in self.edge_list:
            edge.draw()

    def _setup_voxel_neighbors(self):
        print "setup neighbors:"
        for key, voxel in self._voxel_dict.items():
            print "voxel:"+str(voxel)+" at "+str(key)
            for edge_id in range(voxel._voxel_edges.__len__()):
                print "\tedge "+str(edge_id)
                neighbor_keys = voxel.neighbor_keys_of_edge(edge_id)
                for neighbor_key in neighbor_keys:
                    if neighbor_key in self._voxel_dict:
                        print "\t\thas neighbor "+str(self._voxel_dict[neighbor_key])+" at "+str(neighbor_key)
                        voxel.add_neighbor_voxel(edge_id, self._voxel_dict[neighbor_key])


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


class VoxelManager3(AbstractVoxelManager):
    _dimension = 3

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
        self._ax = ax
        for key, vox in self._voxel_dict.items():
            print type(vox)
            vox.set_ax(ax)


