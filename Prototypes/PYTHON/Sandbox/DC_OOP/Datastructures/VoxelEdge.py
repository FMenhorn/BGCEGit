import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from Edge import Edge2, Edge3
from Quad import Quad
from QuadEdgeManager import QuadEdgeManager

__author__ = 'benjamin'


def find_root_bisection(dataset, dp0, dp1):
    position_half = (dp0.get_position() + dp1.get_position())/2.0
    v0 = dp0.get_value()
    v1 = dp1.get_value()
    dp_half = dataset.get_datapoint_at(position_half)
    while dp_half is not None:
        v_half = dp_half.get_value()
        if v_half == v0:
            dp0 = dp_half
        elif v_half == v1:
            dp1 = dp_half
        else:
            raise Exception("class AbstractVoxel::find_root_biscetion\n\t" +
                            "something went wrong in the bisection algorithm!")
        position_half = (dp0.get_position() + dp1.get_position())/2.0
        dp_half = dataset.get_datapoint_at(position_half)

    #gradient = (estimate_gradient_at(dataset, dp0) + estimate_gradient_at(dataset, dp1))/2.0

    return position_half#, gradient

def estimate_gradient_at(dataset, datapoint):
    gradient = np.zeros(2)

    position = datapoint.get_position()

    neighbor_xplus = dataset.get_datapoint_at(position + dataset.get_resolution() * np.array([+1,0]))
    neighbor_xminus = dataset.get_datapoint_at(position + dataset.get_resolution() * np.array([-1,0]))
    neighbor_yplus = dataset.get_datapoint_at(position + dataset.get_resolution() * np.array([0,+1]))
    neighbor_yminus = dataset.get_datapoint_at(position + dataset.get_resolution() * np.array([0,-1]))

    if neighbor_xplus is not None and neighbor_xminus is not None:
        xplus_value = neighbor_xplus.get_value()
        xminus_value = neighbor_xminus.get_value()
    elif neighbor_xminus is not None:
        xplus_value = datapoint.get_value()
        xminus_value = neighbor_xminus.get_value()
    elif neighbor_xplus is not None:
        xplus_value = neighbor_xplus.get_value()
        xminus_value = datapoint.get_value()
    else:
        raise Exception("ERROR in gradient calculation!")

    if neighbor_yplus is not None and neighbor_yminus is not None:
        yplus_value = neighbor_yplus.get_value()
        yminus_value = neighbor_yminus.get_value()
    elif neighbor_yminus is not None:
        yplus_value = datapoint.get_value()
        yminus_value = neighbor_yminus.get_value()
    elif neighbor_yplus is not None:
        yplus_value = neighbor_yplus.get_value()
        yminus_value = datapoint.get_value()
    else:
        raise Exception("ERROR in gradient calculation!")

    if isinstance(xplus_value, bool):
        xplus_value = float(xplus_value)
        xminus_value = float(xminus_value)
        yplus_value = float(yplus_value)
        yminus_value = float(yminus_value)
    elif isinstance(xplus_value, float):
        xplus_value = float(xplus_value<0)
        xminus_value = float(xminus_value<0)
        yplus_value = float(yplus_value<0)
        yminus_value = float(yminus_value<0)
    else:
        raise Exception("unknown datatype!")

    gradient[1] = yplus_value - yminus_value
    gradient[0] = xplus_value - xminus_value

    l_gradient = np.linalg.norm(gradient)
    if l_gradient != 0:
        return gradient / l_gradient
    else:
        return np.zeros(2)


class AbstractVoxelEdge(object):
    _id_counter = 0

    def __init__(self, edge_length, datapoints):
        self._edge_length = edge_length
        self._datapoints = 2 * [None]
        self._is_drawn = False
        self._root_position = None
        # self._root_gradient = None
        for i in range(2):
            self._datapoints[i] = datapoints[i]
        self._id = self._obtain_id()

    def _obtain_id(self):
        id = AbstractVoxelEdge._id_counter
        AbstractVoxelEdge._id_counter += 1
        return id

    def get_id(self):
        return self._id

    def has_signchange(self):
        values = 2 * [None]
        signs = 2 * [None]
        for i in range(2):
            values[i] = self._datapoints[i].get_value()
            if isinstance(values[i], bool):
                signs[i] = values[i]
            elif isinstance(values[i], float):
                signs[i] = values[i] < 0

        return values[0] != values[1]

    def calculate_root(self, dataset):
        dp0 = self._datapoints[0]
        dp1 = self._datapoints[1]
        if self._root_position is None:
            #self._root_position, self._root_gradient = find_root_bisection(dataset, dp0, dp1)
            self._root_position = find_root_bisection(dataset, dp0, dp1)

        return self._root_position#, self._root_gradient

    def link_to(self, vertex_DC, link_id):
        if self._linked_to[link_id] is None:
            self._linked_to[link_id] = vertex_DC
        else:
            raise Exception("overwriting existing link! Something went wrong.")


class VoxelEdge2(AbstractVoxelEdge):

    def __init__(self, edge_length, datapoints):
        self._linked_to = 2 * [None]  # vertices _linked_to are ordered in ascending coordinate direction
        super(VoxelEdge2, self).__init__(edge_length, datapoints)

    def create_dc_edge(self):
        print self._linked_to
        if self._linked_to[0] != None \
                and self._linked_to[1] != None:
            return Edge2(self._linked_to[0], self._linked_to[1])
        else:
            return None

    def draw(self):
        dp0 = self._datapoints[0]
        dp1 = self._datapoints[1]

        pos0 = dp0.get_position()
        pos1 = dp1.get_position()

        root = self._root_position
        gradient = self._root_gradient

        if not self._is_drawn:
            x = [pos0[0],pos1[0]]
            y = [pos0[1],pos1[1]]

            plt.plot(x,y,'k-')
            if root is not None:
                plt.plot(root[0],root[1],'go')
                plt.quiver(root[0],root[1],gradient[0],gradient[1], scale = 10.0 / self._edge_length, width = 0.0025)

            self._is_drawn = True


class VoxelEdge3(AbstractVoxelEdge):
    # ax where plots are created
    _ax = None

    _quad_edge_manager = QuadEdgeManager()

    def __init__(self, edge_length, datapoints):
        self._linked_to = 4 * [None]  # vertices linked to are ordered in CCW direction
        super(VoxelEdge3, self).__init__(edge_length, datapoints)

    def create_dc_quad(self):
        if self._linked_to[0] != None \
                and self._linked_to[1] != None \
                and self._linked_to[2] != None \
                and self._linked_to[3] != None:
            quad_edges = 4 * [None]
            for i in range(4):
                vertex_pair = [self._linked_to[i], self._linked_to[(i+1)%4]]
                quad_edges[i] = VoxelEdge3._quad_edge_manager.get_quad_edge(vertex_pair)

            return Quad(self._linked_to[0], self._linked_to[1], self._linked_to[2], self._linked_to[3],
                        quad_edges[0], quad_edges[1], quad_edges[2], quad_edges[3])
        else:
            return None

    def set_ax(self, ax):
        VoxelEdge3._ax = ax

    def draw(self):
        if not self._is_drawn:
            dp0 = self._datapoints[0]
            dp1 = self._datapoints[1]

            pos0 = dp0.get_position()
            pos1 = dp1.get_position()

            x = [pos0[0],pos1[0]]
            y = [pos0[1],pos1[1]]
            z = [pos0[2],pos1[2]]

            vtx = [zip(x,y,z)]

            edge = Line3DCollection(vtx)
            edge.set_color('k')
            VoxelEdge3._ax.add_collection3d(edge)

            self._is_drawn = True
