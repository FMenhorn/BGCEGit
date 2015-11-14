import numpy as np
import numpy.linalg as la
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from Vertex import VertexDC2, VertexDC3
from VoxelEdgeManager import VoxelEdgeManager2, VoxelEdgeManager3

__author__ = 'benjamin'

from Point import Point


def signs_to_id(signs):
    return sum(1 << i for i, b in enumerate(signs) if b)


class AbstractVoxel(object): # todo reimplement with PYTHON way of defining abstract classes!
    # triggers the behavior of the voxel class, if datapoints for the voxel do not exist
    _create_datapoints_if_they_do_not_exist = True

    _dimension = None

    _voxel_edge_manager = None

    _voxel_verts = None
    _voxel_edges = None

    _vertex_mode = "MEAN_VALUE_MODE"
    _look_up_mode = "LAZY"

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

    def get_gradients(self):
        gradients = {}
        for local_id, dp in self._voxel_datapoints.items():
            gradients[local_id] = self._estimate_gradient_on_vertex(local_id)
        return gradients

    def _get_middle_position(self):
        displacement = np.ones(self.__class__._dimension)
        return self._origin.get_position() + self._edge_length / 2 * displacement

    def _get_middle_point(self):
        middle_position = self._get_middle_position()
        return self._dataset.get_datapoint_at(middle_position)

    def _estimate_gradient_on_vertex(self, local_id):
        neighbor_disps= [np.array([1,1]),
                         np.array([-1,-1]),
                         np.array([-1,1]),
                         np.array([1,-1])]

        point = self._voxel_datapoints[local_id]

        gradient = np.zeros(2)
        for neighbor_disp in neighbor_disps:
            neighbor_pos = point.get_position() + self._edge_length / 2.0 * neighbor_disp
            neighbor = self._dataset.get_datapoint_at(neighbor_pos)
            if neighbor is not None:
                gradient += (float(neighbor.get_value()) - float(point.get_value())) * neighbor_disp

        return gradient / 4.0

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
        #sign_change_gradients = {}

        for local_edge_ids in sign_change_edges:
            sign_change_edge = self._voxel_dataedges[local_edge_ids]
            #root_position, gradient = sign_change_edge.calculate_root(self._dataset)
            root_position = sign_change_edge.calculate_root(self._dataset)
            sign_change_roots[local_edge_ids] = root_position
            #sign_change_gradients[local_edge_ids] = gradient

        return sign_change_roots#, sign_change_gradients

    def generate_dc_vertices(self):
        #root_positions, gradients = self._get_roots_sign_change_edges() # calculate roots in voxel
        root_positions = self._get_roots_sign_change_edges() # calculate roots in voxel

        n_roots = 0
        hermite_data = []
        for edge_id, root_position in root_positions.items(): # extract hermite data
            root = root_position
            #normal = gradients[edge_id]
            #hermite_data.append((root, normal))
            hermite_data.append((root))
            n_roots += 1

        if n_roots > 0: # found at least one sign change edge. Generate proper number of DC vertices in voxel

            mc_case_id = self._get_mc_case_id() # transform binary vector with signs to id of marching cubes case

            if self._look_up_mode == "LAZY":  # treat only ambiguous cases corresponding to marching cubes look up table
                if mc_case_id in self._lazy_marching_cubes_look_up_table:  # is ambiguous case
                    case_connectivity = self._lazy_marching_cubes_look_up_table[mc_case_id]
                    n_vertices = case_connectivity.__len__()  # number of vertices, which will be generated.
                else:  # no ambigous case, only one vertex needed
                    case_connectivity = [tuple(root_positions.keys())]
                    n_vertices = 1
            else: # treat any case corresponding to marching cubes look up table
                case_connectivity = self._marching_cubes_look_up_table[mc_case_id]
                n_vertices = case_connectivity.__len__() # number of vertices, which will be generated.

            connectivity = n_vertices * [None] # list of connectivities for each vertex
            new_vertices = n_vertices * [None] # list of new vertices

            for vertex_id in range(n_vertices):  # generate necessary vertices
                new_vertices[vertex_id] = np.zeros([self._dimension])  # initialize each new vertex with zero vector

                if self._vertex_mode == "LEAST_SQUARES_MODE":  # calculate vertex position by minimizing QEF
                    raise Exception("not implemented!")
                    # #build least squares system:
                    # A = [ normal.tolist() for root, normal in hermite_data]
                    # b = [ np.dot(normal, root) for root, normal in hermite_data]
                    # #solve system
                    # v, residue, rank, s = la.lstsq(A, b)
                    # vertex_position = np.array(v)
                elif self._vertex_mode == "MEAN_VALUE_MODE":  # calculate vertex position by taking mean value of roots
                    connection = case_connectivity[vertex_id]  # get edge connection for this vertex
                    connectivity[vertex_id] = []  # initialize connectivity list
                    for edge_id in connection:  # calculate mean value
                        new_vertices[vertex_id] += root_positions[edge_id]  # sum up roots
                        root_edge = self._voxel_dataedges[edge_id]  # edge object which contains this root
                        link_id = self._get_link_id(edge_id)
                        connectivity[vertex_id].append((link_id,root_edge))  # add edge to connectivity of new vertex
                    new_vertices[vertex_id] /= connection.__len__()  # divide by number of roots
                    self._add_vertex(new_vertices[vertex_id], connectivity[vertex_id])  # add new vertex to voxel
                else:
                    raise Exception('no supported mode selected!')

    def _add_vertex(self, vertex, connectivity):
        raise Exception("Abstract method, not implemented!")

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
    # automate LUT generation! one nice property: complement is equal! Be careful with ambiguities!
    _marching_cubes_look_up_table = {0: [],
                                     1: [(0,3)],
                                     2: [(0,1)],
                                     3: [(1,3)],
                                     4: [(1,2)],
                                     #5: [(0,3),(1,2)], # split
                                     5: [(0,1),(2,3)], # join
                                     #5: [(0,1,2,3)], # ambiguous case!
                                     6: [(0,2)],
                                     7: [(2,3)], # here is symmetry
                                     8: [(2,3)],
                                     9: [(0,2)],
                                     #10:[(0,1),(2,3)], # split
                                     10:[(0,3),(1,2)], # join
                                     #10:[(0,1,2,3)], # ambiguous case!
                                     11:[(1,2)],
                                     12:[(1,3)],
                                     13:[(0,1)],
                                     14:[(0,3)],
                                     15:[]
                                     }

    _lazy_marching_cubes_look_up_table = {#5: [(0,3),(1,2)], # split
                                          5: [(0,1),(2,3)], # join
                                          #5: [(0,1,2,3)], # ambiguous case!
                                          #10:[(0,1),(2,3)] # split
                                          10:[(0,3),(1,2)] # join
                                          #10:[(0,1,2,3)] # ambiguous case!
                                          }

    def __init__(self, origin, edge_length, dataset):
        super(Voxel2, self).__init__(origin, edge_length, dataset)

    def _add_vertex(self, position, connectivity):
        vertex = VertexDC2(position[0], position[1], connectivity)
        self._dc_vertices.append(vertex)

    def _get_link_id(self, edge_id):
        if edge_id == 1 or edge_id == 2:
            return 0
        else:
            return 1

    def _get_mc_case_id(self):
        signs_list = 4 * [None]
        signs_dict = self.get_signs()

        for i,s in signs_dict.items():
            signs_list[i] = s

        return signs_to_id(signs_list)


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
                    11:(3,7)} # traverse verts of voxel in CCW manner, first z = 0, then z = 1 plane, then connections

    _dimension = 3

    _voxel_edge_manager = VoxelEdgeManager3()

    _lazy_marching_cubes_look_up_table = {}

    def __init__(self, origin, edge_length, dataset):
        super(Voxel3, self).__init__(origin, edge_length, dataset)

    def _add_vertex(self, position, connectivity):
        vertex = VertexDC3(position[0], position[1], position[2], connectivity)
        self._dc_vertices.append(vertex)

    def set_ax(self, ax):
        Voxel3._ax = ax
        self._voxel_edge_manager.set_ax(ax)

    def _get_link_id(self, edge_id):
        if edge_id == 10 or edge_id == 1 or edge_id == 0:
            return 0
        elif edge_id == 11 or edge_id == 3 or edge_id == 2:
            return 1
        elif edge_id == 8 or edge_id == 7 or edge_id == 6:
            return 2
        elif edge_id == 9 or edge_id == 5 or edge_id == 4:
            return 3
        else:
            raise Exception("invalid edge id!")

    def _get_mc_case_id(self):
        signs_list = 8 * [None]
        signs_dict = self.get_signs()

        for i,s in signs_dict.items():
            signs_list[i] = s

        return signs_to_id(signs_list)


class VoxelFace(object):
    # ax where plots are created
    _ax = None

    def __init__(self, face_edges):
        for i in range(2):
            self._face_edges[i] = face_edges[i]

    def set_ax(self, ax):
        VoxelFace._ax = ax