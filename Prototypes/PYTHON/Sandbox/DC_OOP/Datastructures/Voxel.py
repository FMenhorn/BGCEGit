import numpy as np

__author__ = 'benjamin'

from BasicDatastructures import Point


class AbstractVoxel(object): # todo reimplement with PYTHON way of defining abstract classes!
    # triggers the behavior of the voxel class, if datapoints for the voxel do not exist
    _create_datapoints_if_they_do_not_exist = True

    _voxel_verts = None
    _voxel_edges = None
    _dimension = None

    def __init__(self, origin, edge_length, dataset):
        self._origin = Point(origin)
        self._edge_length = edge_length
        self._set_voxel_datapoints(dataset)

    def _set_voxel_datapoints(self, dataset):
        self._voxel_datapoints = {}

        for local_id, vec_origin_corner in self._voxel_verts.items():
            corner_position = self._origin.get_position() + \
                              self._edge_length * vec_origin_corner
            if dataset.datapoint_at_exists(corner_position):
                self._voxel_datapoints[local_id] = dataset.get_datapoint_at(corner_position)
            elif self._create_datapoints_if_they_do_not_exist:
                dataset.add_datapoint(corner_position, False)
                self._voxel_datapoints[local_id] = dataset.get_datapoint_at(corner_position)
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
                raise Exception("class __AbstractVoxel::get_signs\n\tinvalid value format in datapoint!")

        return signs

    def get_sign_change_edges(self):
        sign_change_edges = {}
        signs = self.get_signs()
        if np.array(signs.values()).all() or not np.array(signs.values()).any():
            return sign_change_edges
        else:
            for local_edge_id, edge_key in self._voxel_edges.items():
                print "IMPLEMENT HERE!"
                quit()



class Voxel2(AbstractVoxel):
    # Vertices of quad
    _voxel_verts = {0: np.array([0.0, 0.0]),
                    1: np.array([1.0, 0.0]),
                    2: np.array([1.0, 1.0]),
                    3: np.array([0.0, 1.0])}  # traverse verts  of voxel in CCW manner

    _voxel_edges = {0: (0,1),
                    1: (1,2),
                    2: (2,3),
                    3: (3,0)} # traverse edges of voxel in CCW manner, starting at bottom edge

    _dimension = 2

    def __init__(self, origin, edge_length, dataset):
        super(Voxel2, self).__init__(origin, edge_length, dataset)


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

    _dimension = 3

    def __init__(self, origin, edge_length, dataset):
        super(Voxel3, self).__init__(origin, edge_length, dataset)