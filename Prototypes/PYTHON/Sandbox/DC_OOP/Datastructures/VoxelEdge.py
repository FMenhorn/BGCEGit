import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from Edge import Edge2, Edge3

__author__ = 'benjamin'


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


class AbstractVoxelEdge(object):
    _id_counter = 0

    def __init__(self, edge_length, datapoints):
        self._edge_length = edge_length
        self._datapoints = 2 * [None]
        self._is_drawn = False
        for i in range(2):
            self._datapoints[i] = datapoints[i]
        self._id = self._obtain_id()
        self._linked_to = []

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

        return find_root_bisection(dataset, dp0, dp1)

    def link_to(self, vertexDC):
        self._linked_to.append(vertexDC)


class VoxelEdge2(AbstractVoxelEdge):
    def __init__(self, edge_length, datapoints):
        super(VoxelEdge2, self).__init__(edge_length, datapoints)

    def draw(self):
        dp0 = self._datapoints[0]
        dp1 = self._datapoints[1]

        pos0 = dp0.get_position()
        pos1 = dp1.get_position()

        if not self._is_drawn:
            x = [pos0[0],pos1[0]]
            y = [pos0[1],pos1[1]]

            plt.plot(x,y,'k-')

            self._is_drawn = True

    def create_dc_edge(self):
        print self._linked_to
        if self._linked_to.__len__() > 0:
            return Edge2(self._linked_to[0], self._linked_to[1])
        else:
            return None


class VoxelEdge3(AbstractVoxelEdge):
    # ax where plots are created
    _ax = None

    def __init__(self, edge_length, datapoints):
        super(VoxelEdge3, self).__init__(edge_length, datapoints)

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
