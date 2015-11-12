from VoxelEdge import VoxelEdge2, VoxelEdge3

__author__ = 'benjamin'


class AbstractVoxelEdgeManager(object):
    def __init__(self):
        self._edgedict = {}

    def get_voxel_edge(self, edge_length, datapoints):
        key = tuple({datapoints[0], datapoints[1]})
        id_key = tuple(sorted([key[0].get_id(),key[1].get_id()]))
        if id_key in self._edgedict: # edge already in manager
            return self._edgedict[id_key]
        else: # create new edge in manager
            new_edge = self._create_voxel_edge(edge_length, datapoints)
            self._edgedict[id_key] = new_edge
            return new_edge


class VoxelEdgeManager2(AbstractVoxelEdgeManager):
    def _create_voxel_edge(self, edge_length, datapoints):
        return VoxelEdge2(edge_length, datapoints)

    def create_all_dc_edges(self):
        dc_edgelist = []
        for key, edge in self._edgedict.items():
            dc_edge = edge.create_dc_edge()
            if dc_edge is not None:
                dc_edgelist.append(dc_edge)

        return dc_edgelist


class VoxelEdgeManager3(AbstractVoxelEdgeManager):
    _ax = None

    def _create_voxel_edge(self, edge_length, datapoints):
        return VoxelEdge3(edge_length, datapoints)

    def create_all_dc_quads(self):
        dc_quadlist = []
        for key, edge in self._edgedict.items():
            dc_quad = edge.create_dc_quad()
            if dc_quad is not None:
                dc_quadlist.append(dc_quad)

        return dc_quadlist

    def set_ax(self, ax):
        VoxelEdgeManager3._ax = ax
        for key, ve in self._edgedict.items():
            ve.set_ax(ax)
