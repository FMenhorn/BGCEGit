import numpy as np
from Vertex import VertexDC2, VertexDC3
from VoxelEdgeManager import VoxelEdgeManager2, VoxelEdgeManager3

__author__ = 'benjamin'

from Point import Point


class AbstractVoxel(object): # todo reimplement with PYTHON way of defining abstract classes!
    # triggers the behavior of the voxel class, if datapoints for the voxel do not exist
    _create_datapoints_if_they_do_not_exist = True

    _dimension = None

    _voxel_edge_manager = None

    _voxel_verts = None
    _voxel_edges = None

    def __init__(self, origin, edge_length, dataset):
        self._origin = Point(origin)
        self._edge_length = edge_length
        self._dataset = dataset
        self._set_voxel_datapoints()
        self._set_voxel_dataedges()
        self._dc_vertices = []

    def get_origin(self):
        return self._origin.get_position()

    def get_dc_vertices(self):
        return self._dc_vertices

    def _set_voxel_datapoints(self):
        self._voxel_datapoints = {}
        for local_id, vec_origin_corner in self.__class__._voxel_verts.items():
            corner_position = self._origin.get_position() + \
                              self._edge_length * vec_origin_corner
            if self._dataset.datapoint_at_exists(corner_position):
                self._voxel_datapoints[local_id] = self._dataset.get_datapoint_at(corner_position)
            elif self._create_datapoints_if_they_do_not_exist:
                self._dataset.add_datapoint(corner_position, False)
                self._voxel_datapoints[local_id] = self._dataset.get_datapoint_at(corner_position)
            else:
                expt_str = "class __AbstractVoxel::__set_voxel_data\n\tDatapoint at "+str(corner_position)+"does not exist!"
                raise Exception(expt_str)

    def _set_voxel_dataedges(self):
        self._voxel_dataedges = {}
        for local_id, local_edge_key in self.__class__._voxel_edges.items():
            datapoints = 2 * [None]
            for i in range(2):
                datapoints[i] = self._voxel_datapoints[local_edge_key[i]]

            self._voxel_dataedges[local_id] = self.__class__._voxel_edge_manager.get_voxel_edge(self._edge_length, datapoints)

    def get_signs(self):
        signs = {}
        for local_id, datapoint in self._voxel_datapoints.items():
            value = self._voxel_datapoints[local_id].get_value()
            if isinstance(value, bool):
                signs[local_id] = value
            elif isinstance(value, float):
                signs[local_id] = value < 0
            else:
                raise Exception("class __AbstractVoxel::get_signs\n\tinvalid value format in datapoint!")

        return signs

    def _get_sign_change_edges(self):
        sign_change_edges = set()
        signs = self.get_signs()
        if np.array(signs.values()).all() or not np.array(signs.values()).any():
            return sign_change_edges
        else:
            for local_edge_id, dataedge in self._voxel_dataedges.items():
                if dataedge.has_signchange():
                    sign_change_edges.add(local_edge_id)
            return sign_change_edges

    def _get_roots_sign_change_edges(self):
        sign_change_edges = self._get_sign_change_edges()
        sign_change_roots = {}

        for local_edge_ids in sign_change_edges:
            sign_change_edge = self._voxel_dataedges[local_edge_ids]
            sign_change_roots[local_edge_ids] = sign_change_edge.calculate_root(self._dataset)

        return sign_change_roots

    def generate_dc_vertices(self):
        root_positions = self._get_roots_sign_change_edges()
        vertex_position = np.zeros([self._dimension])
        connectivity = []
        n_roots = 0
        for edge_id, root_position in root_positions.items():
            vertex_position += root_position
            n_roots += 1
            connectivity.append(self._voxel_dataedges[edge_id])

        if n_roots != 0:
            vertex_position /= n_roots
            self._add_vertex_at(vertex_position, connectivity)

    def _add_vertex(self, vertex):
        self._dc_vertices.append(vertex)

    def draw(self):
        for local_vert_id, datapoint in self._voxel_datapoints.items():
            datapoint.draw()
        for local_edge_id, edge in self._voxel_dataedges.items():
            edge.draw()


class Voxel2(AbstractVoxel):
    # Vertices of quad
    _voxel_verts = {0: np.array([0.0, 0.0]),
                    1: np.array([1.0, 0.0]),
                    2: np.array([1.0, 1.0]),
                    3: np.array([0.0, 1.0])}  # traverse verts  of voxel in CCW manner

    _voxel_edges = {0: (0, 1),
                    1: (1, 2),
                    2: (2, 3),
                    3: (3, 0)} # traverse edges of voxel in CCW manner, starting at bottom edge

    _dimension = 2

    _voxel_edge_manager = VoxelEdgeManager2()

    def __init__(self, origin, edge_length, dataset):
        super(Voxel2, self).__init__(origin, edge_length, dataset)

    def _add_vertex_at(self, position, connectivity):
        vertex = VertexDC2(position[0], position[1], connectivity)
        super(Voxel2,self)._add_vertex(vertex)

    def _set_dataedge(self, local_edge_id):
        dp0 = self._voxel_datapoints[local_edge_id[0]]
        dp1 = self._voxel_datapoints[local_edge_id[1]]
        key = tuple({dp0,dp1}) # transform set {dp0,dp1} to tuple to destroy ordering and get hashable key
        if key in self._dataedge_set:
            return self._dataedge_set[key]
        else:
            self._dataedge_set.add_edge(key,dp0,dp1)
            return self._dataedge_set[key]

#todo class not fully implemented!
class Voxel3(AbstractVoxel):
    # ax where plots are created
    _ax = None

    # Vertices if cube
    _voxel_verts = {0: np.array([0.0, 0.0, 0.0]),
                    1: np.array([1.0, 0.0, 0.0]),
                    2: np.array([1.0, 1.0, 0.0]),
                    3: np.array([0.0, 1.0, 0.0]),
                    4: np.array([0.0, 0.0, 1.0]),
                    5: np.array([1.0, 0.0, 1.0]),
                    6: np.array([1.0, 1.0, 1.0]),
                    7: np.array([0.0, 1.0, 1.0])}  # traverse verts  of voxel in CCW manner, first z = 0, then z = 1 plane

    _voxel_edges = {0: (0,1),
                    1: (1,2),
                    2: (2,3),
                    3: (3,0),
                    4: (4,5),
                    5: (5,6),
                    6: (6,7),
                    7: (7,4),
                    8: (0,4),
                    9: (1,5),
                    10:(2,6),
                    11:(3,7)} # traverse verts  of voxel in CCW manner, first z = 0, then z = 1 plane, then connections

    _dimension = 3

    _voxel_edge_manager = VoxelEdgeManager3()

    def __init__(self, origin, edge_length, dataset):
        super(Voxel3, self).__init__(origin, edge_length, dataset)

    def _add_vertex_at(self, position, connectivity):
        vertex = VertexDC3(position[0], position[1], position[2], connectivity)
        super(Voxel3,self)._add_vertex(vertex)

    def set_ax(self, ax):
        Voxel3._ax = ax
#todo !!!!!!!!!
    def _set_dataedge(self, local_edge_id):
        dp0 = self._voxel_datapoints[local_edge_id[0]]
        dp1 = self._voxel_datapoints[local_edge_id[1]]
        return VoxelEdge3(self._edge_length,[dp0,dp1])

class VoxelFace(object):
    # ax where plots are created
    _ax = None

    def __init__(self, face_edges):
        for i in range(2):
            self._face_edges[i] = face_edges[i]

    def set_ax(self, ax):
        VoxelFace._ax = ax