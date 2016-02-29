import itertools as it
import numpy as np


def voxel(edge_length, center):
    center = np.array(center)
    scale = 1
    x0 = (center + edge_length * scale * .5 * np.array([-1, -1, -1])).tolist()
    x1 = (center + edge_length * scale * .5 * np.array([-1, 1, -1])).tolist()
    x2 = (center + edge_length * scale * .5 * np.array([1, 1, -1])).tolist()
    x3 = (center + edge_length * scale * .5 * np.array([1, -1, -1])).tolist()
    x4 = (center + edge_length * scale * .5 * np.array([-1, -1, 1])).tolist()
    x5 = (center + edge_length * scale * .5 * np.array([-1, 1, 1])).tolist()
    x6 = (center + edge_length * scale * .5 * np.array([1, 1, 1])).tolist()
    x7 = (center + edge_length * scale * .5 * np.array([1, -1, 1])).tolist()

    return [[x0, x1, x2, x3, x0],
            [x4, x5, x6, x7, x4],
            [x0, x1, x5, x4, x0],
            [x2, x3, x7, x6, x2],
            [x0, x3, x7, x4, x0],
            [x1, x2, x6, x5, x1]]


def parse_dims(dims, res):
    if dims.__len__() == 6:
        dims_return = {'min': 3 * [None], 'max': 3 * [None]}
        dims_return['min'][0] = dims['xmin']
        dims_return['min'][1] = dims['ymin']
        dims_return['min'][2] = dims['zmin']
        dims_return['max'][0] = dims['xmax']
        dims_return['max'][1] = dims['ymax']
        dims_return['max'][2] = dims['zmax']
    elif dims.__len__() == 2:
        dims_return = dims
    else:
        raise Exception("dims has wrong length!")

    for d in range(3):  # check if dimensions match with resolution
        gap = (dims_return['max'][d] - dims_return['min'][d]) % res  # if dimensions match, this is equal to 0!
        dims_return['max'][d] += (res - gap) % res

    return dims_return


def parse_dataset(dataset):
    if type(dataset) is set:
        return_dataset = dataset
    elif type(dataset) is dict:
        return_dataset = set()
        for key, value in dataset.items():
            if value == -1:
                return_dataset.add(key)
    else:
        raise Exception("dataset of wrong type!")

    return return_dataset


class VoxelDataset():

    def __init__(self, dims, resolution, dataset):
        assert type(dims) is dict
        self._dimensions = parse_dims(dims, resolution)

        assert type(resolution) is int
        assert resolution >= 1
        self._resolution = int(resolution)

        self._dataset = parse_dataset(dataset)

    def point_is_inside(self, point):
        assert type(point) is tuple
        assert point.__len__() == 3

        for d in range(3):
            if not (self._dimensions['min'][d] <= point[d] <= self._dimensions['max'][d]):
                # point is in one dimensions not inside
                return False
        # point is in all dimensions inside bounding box
        return True

    def point_is_aligned(self, point):
        assert type(point) is tuple
        assert point.__len__() == 3

        for d in range(3):
            if (abs(point[d] - self._dimensions['min'][d]) % (self._resolution * .5)) != 0:  # point is not aligned
                return False
        # all points are obviously aligned
        return True

    def valid_point(self, point):
        assert type(point) is tuple
        assert point.__len__() == 3

        if not self.point_is_inside(point):
            return False
        else:
            return True

    def value_at(self, point):
        if self.valid_point(point):
            return point in self._dataset
        else:
            if not self.point_is_inside(point):
                raise Exception("invalid point! Point %s is not inside %s." % (point, self._dimensions))

    def __getitem__(self, item):
        assert type(item) is tuple
        assert item.__len__() == 3
        return self.value_at(item)

    def get_grid_iterator(self):
        """
        :return: Iterator for the grid of the dataset.
        """
        return it.product(np.arange(self._dimensions['min'][0], self._dimensions['max'][0], self._resolution),
                          np.arange(self._dimensions['min'][1], self._dimensions['max'][1], self._resolution),
                          np.arange(self._dimensions['min'][2], self._dimensions['max'][2], self._resolution))

    def get_total_voxels(self):
        return np.arange(self._dimensions['min'][0], self._dimensions['max'][0], self._resolution).__len__() * \
               np.arange(self._dimensions['min'][1], self._dimensions['max'][1], self._resolution).__len__() * \
               np.arange(self._dimensions['min'][2], self._dimensions['max'][2], self._resolution).__len__()


    def plot(self, axis, color, alpha):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
        for x, y, z in self.get_grid_iterator():
            key = (x, y, z)
            if key in self._dataset:
                voxel_data = voxel(edge_length=self._resolution, center=key)
                if alpha != 0:
                    vox = Poly3DCollection(voxel_data)
                    vox.set_color(color)
                    vox.set_alpha(alpha)
                    vox.set_edgecolor('k')
                    axis.add_collection3d(vox)
                else:
                    mesh = Line3DCollection(voxel_data,colors=color)
                    axis.add_collection3d(mesh)