import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from Vertex import VertexDC2, VertexDC3

__author__ = 'benjamin'

from BasicDatastructures import Point

def find_root_bisection(dataset, dp0, dp1):
    position_half = (dp0.get_position() + dp1.get_position())/2.0
    v0 = dp0.get_value()
    v1 = dp1.get_value()
    while dataset.datapoint_at_exists(position_half):
        dp_half = dataset.get_datapoint_at(position_half)
        v_half = dp_half.get_value()
        if v_half == v0:
            dp0 = dp_half
        elif v_half == v1:
            dp1 = dp_half
        else:
            raise Exception("class AbstractVoxel::find_root_biscetion\n\t" +
                            "something went wrong in the bisection algorithm!")
        position_half = (dp0.get_position() + dp1.get_position())/2.0

    return position_half

class AbstractVoxel(object): # todo reimplement with PYTHON way of defining abstract classes!
    # triggers the behavior of the voxel class, if datapoints for the voxel do not exist
    _create_datapoints_if_they_do_not_exist = True

    _dimension = None

    _dc_vertex_id = 0

    _voxel_verts = None
    _voxel_edges = None
    _voxel_neighbor_origin = None

    def __init__(self, origin, edge_length, dataset):
        self._origin = Point(origin)
        self._edge_length = edge_length
        self._dataset = dataset
        self._set_voxel_datapoints()
        self._dc_vertices = []
        self._edge_neighbor_voxels = {}
        for i in range(self._voxel_edges.__len__()):
            self._edge_neighbor_voxels[i] = []

    def get_origin(self):
        return self._origin.get_position()

    def get_dc_vertices(self):
        return self._dc_vertices

    def _set_voxel_datapoints(self):
        self._voxel_datapoints = {}
        for local_id, vec_origin_corner in self._voxel_verts.items():
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

    def get_signs(self):
        signs = {}
        for local_id, datapoint in self._voxel_datapoints.items():
            value = self._voxel_datapoints[local_id].get_value()
            if isinstance(value, bool):
                signs[local_id] = value
            elif isinstance(value, float):
                signs[local_id] = value < 0
            else:
                print type(value)
                raise Exception("class __AbstractVoxel::get_signs\n\tinvalid value format in datapoint!")

        return signs

    def _get_sign_change_edges(self):
        sign_change_edges = set()
        signs = self.get_signs()
        if np.array(signs.values()).all() or not np.array(signs.values()).any():
            return sign_change_edges
        else:
            for local_edge_id, edge_key in self._voxel_edges.items():
                if signs[edge_key[0]] != signs[edge_key[1]]:
                    sign_change_edges.add(local_edge_id)
            return sign_change_edges

    def _get_roots_sign_change_edges(self):
        sign_change_edges = self._get_sign_change_edges()
        sign_change_roots = {}

        for local_edge_ids in sign_change_edges:
            sign_change_roots[local_edge_ids] = self._calculate_root_on_edge(local_edge_ids)

        return sign_change_roots

    def _calculate_root_on_edge(self, local_edge_id):
        local_corner_ids = self._voxel_edges[local_edge_id]
        start_corner_id = local_corner_ids[0]
        end_corner_id = local_corner_ids[1]
        dp0 = self._voxel_datapoints[start_corner_id]
        dp1 = self._voxel_datapoints[end_corner_id]

        return find_root_bisection(self._dataset, dp0, dp1)

    def generate_dc_vertices(self):
        root_positions = self._get_roots_sign_change_edges()
        vertex_position = np.zeros([self._dimension])
        connectivity = []
        n_roots = 0
        for edge_id, root_position in root_positions.items():
            vertex_position += root_position
            n_roots += 1
            connectivity.append(self._edge_neighbor_voxels[edge_id])

        if n_roots != 0:
            vertex_position /= n_roots
            self._add_vertex_at(vertex_position, connectivity)

    def _add_vertex(self, vertex):
        self._dc_vertices.append(vertex)
        self._dc_vertex_id += 1

    def draw_voxel(self):
        x = []
        y = []
        for local_vert_id, datapoint in self._voxel_datapoints.items():
            self._draw_datapoint(local_vert_id)

        for local_edge_id, edge in self._voxel_edges.items():
            self._draw_edge(local_edge_id)

    def neighbor_keys_of_edge(self, local_edge_id):
        neighbor_keys = []
        for displacement in self._voxel_neighbor_origin[local_edge_id]:
            neighbor_origin = self._origin.get_position() + displacement * self._edge_length
            neighbor_keys.append(tuple(neighbor_origin))

        return neighbor_keys

    def add_neighbor_voxel(self, local_edge_id, voxel):
        print "adding voxel to edge "+str(local_edge_id)+": "+str(voxel)
        self._edge_neighbor_voxels[local_edge_id].append(voxel)
        print self._edge_neighbor_voxels

    def get_neighbor_voxels(self):
        return self._edge_neighbor_voxels


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

    _voxel_neighbor_origin = {0: [np.array([0.0, -1.0])],
                              1: [np.array([1.0, 0.0])],
                              2: [np.array([0.0, 1.0])],
                              3: [np.array([-1.0, 0.0])]} # origins of each edge's neighbor voxel

    _dimension = 2

    def __init__(self, origin, edge_length, dataset):
        super(Voxel2, self).__init__(origin, edge_length, dataset)

    def _add_vertex_at(self, position, connectivity):
        vertex = VertexDC2(self._dc_vertex_id, position[0], position[1], connectivity)
        super(Voxel2,self)._add_vertex(vertex)

    def _draw_datapoint(self, local_id):
        datapoint = self._voxel_datapoints[local_id]
        pos = datapoint.get_position()
        xx = pos[0]
        yy = pos[1]
        if datapoint.get_value() > 0:
            plt.plot(xx,yy,'ro')
        else:
            plt.plot(xx,yy,'bo')

    def _draw_edge(self, local_edge_id):
        local_vert_ids = self._voxel_edges[local_edge_id]
        dp0 = self._voxel_datapoints[local_vert_ids[0]]
        dp1 = self._voxel_datapoints[local_vert_ids[1]]

        pos0 = dp0.get_position()
        pos1 = dp1.get_position()

        x = [pos0[0],pos1[0]]
        y = [pos0[1],pos1[1]]

        plt.plot(x,y,'k-')


#todo class not fully implemented!
class Voxel3(AbstractVoxel):
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

    def __init__(self, origin, edge_length, dataset):
        super(Voxel3, self).__init__(origin, edge_length, dataset)

    def _add_vertex_at(self, position, connectivity):
        vertex = VertexDC3(self._dc_vertex_id, position[0], position[1], position[2], connectivity)
        super(Voxel3,self)._add_vertex(vertex)

    def _draw_datapoint(self, local_id):
        datapoint = self._voxel_datapoints[local_id]
        pos = datapoint.get_position()
        xx = pos[0]
        yy = pos[1]
        zz = pos[2]
        if datapoint.get_value() > 0:
            self._ax.scatter(xx,yy,zz,'ro')
        else:
            self._ax.scatter(xx,yy,zz,'bo')

    def _draw_edge(self, local_edge_id):
        local_vert_ids = self._voxel_edges[local_edge_id]
        dp0 = self._voxel_datapoints[local_vert_ids[0]]
        dp1 = self._voxel_datapoints[local_vert_ids[1]]

        pos0 = dp0.get_position()
        pos1 = dp1.get_position()

        x = [pos0[0],pos1[0]]
        y = [pos0[1],pos1[1]]
        z = [pos0[2],pos1[2]]

        vtx = [zip(x,y,z)]

        edge = Line3DCollection(vtx)
        edge.set_color('k')
        self._ax.add_collection3d(edge)

    def set_ax(self, ax):
        self._ax = ax


def AbstractVoxelEdge(object):
    def __init__(self, edge_length, datapoints):
        self._edge_length = edge_length
        for i in range(2):
            self._datapoints[i] = datapoints[i]


def VoxelEdge2(AbstractVoxelEdge):
    def __init__(self, edge_length, datapoints):
        super(VoxelEdge2, self).__init__(edge_length, datapoints)


def VoxelEdge3(AbstractVoxelEdge):
    def __init__(self, edge_length, datapoints):
        super(VoxelEdge3, self).__init__(edge_length, datapoints)


def VoxelFace(object):
    def __init__(self, face_edges):
        for i in range(2):
            self._face_edges[i] = face_edges[i]