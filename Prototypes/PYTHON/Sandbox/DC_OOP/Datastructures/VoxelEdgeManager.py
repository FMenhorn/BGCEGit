from VoxelEdge import VoxelEdge2, VoxelEdge3

__author__ = 'benjamin'


class AbstractVoxelEdgeManager(object):
    def __init__(self):
        self._edgedict = {}

    def get_voxel_edge(self, edge_length, datapoints):
        key = tuple({datapoints[0], datapoints[1]})
        id_key = tuple(sorted([key[0].get_id(),key[1].get_id()]))
        pos_key = tuple([key[0].get_position(),key[1].get_position()])
        if id_key in self._edgedict: # edge already in manager
            return self._edgedict[id_key]
        else: # create new edge in manager
            new_edge = self.create_voxel_edge(edge_length, datapoints)
            self._edgedict[id_key] = new_edge
            return new_edge

    def create_all_dc_edges(self):
        dc_edgelist = []
        for key, edge in self._edgedict.items():
            dc_edge = edge.create_dc_edge()
            if dc_edge is not None:
                dc_edgelist.append(dc_edge)

        return dc_edgelist



class VoxelEdgeManager2(AbstractVoxelEdgeManager):
    def create_voxel_edge(self, edge_length, datapoints):
        return VoxelEdge2(edge_length, datapoints)


class VoxelEdgeManager3(AbstractVoxelEdgeManager):
    def create_voxel_edge(self, edge_length, datapoints):
        return VoxelEdge3(edge_length, datapoints)
