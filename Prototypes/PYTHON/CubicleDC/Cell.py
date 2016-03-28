import numpy as np


def case1(origin, dir1, dir2):
    return (np.array([origin + .75 * (dir1 + dir2),
                      origin + dir1 + .5 * (dir2),
                      origin + dir2 + .5 * (dir1)]),
            [[0, 1], [0, 2]])


def case1_rot_pos(origin, dir1, dir2):
    return case1(origin+dir2,dir1,-dir2)


def case1_rot_neg(origin, dir1, dir2):
    return case1(origin+dir1,-dir1,dir2)

def case1_mirr(origin,dir1,dir2):
    return case1(origin+dir1+dir2,-dir1,-dir2)


def case2(origin, dir1, dir2):
    return (np.array([origin + .5 * (dir1 + dir2),
                      origin + dir2 + .5 * (dir1),
                      origin + .5 * (dir1)]),
            [[0, 1], [0, 2]])


def case2_mirr(origin, dir1, dir2):
    return case2(origin+dir1+dir2,-dir2,-dir1)

def case2_rot_pos(origin, dir1, dir2):
    return case2(origin+dir2,dir1,-dir2)

def case2_rot_neg(origin, dir1, dir2):
    return case2(origin+dir1,-dir1,dir2)

def case3(origin, dir1, dir2):
    return (np.array([origin + .25 * (dir1 + dir2),
                      origin + .5 * (dir1),
                      origin + .5 * (dir2)]),
            [[0, 1], [0, 2]])

def case3_mirr(origin, dir1, dir2):
    return case3(origin+dir1+dir2,-dir2,-dir1)

def case3_rot_pos(origin, dir1, dir2):
    return case3(origin+dir2,dir1,-dir2)

def case3_rot_neg(origin, dir1, dir2):
    return case3(origin+dir1,-dir1,dir2)

def case4_1(origin, dir1, dir2): # connected!
    return (np.array([origin + .75 * (dir1 + dir2),
                      origin + dir1 + .5 * (dir2),
                      origin + dir2 + .5 * (dir1),
                      origin + .25 * (dir1 + dir2),
                      origin + .5 * (dir1),
                      origin + .5 * (dir2)]),
            [[0, 1], [0, 2], [3, 4], [3, 5]])

def case4_1_mirr(origin, dir1, dir2): # connected!
    return case4_1(origin+dir1,-dir1,dir2)

def case4_2_mirr(origin, dir1, dir2): # notconnected!
    return case4_1(origin+dir1+dir2,-dir2,-dir1)


dc_lut = {
    (False, False, False, True): case1,             #1
    (False, False, True, False): case1_rot_pos,     #2
    (False, False, True, True): case2,              #3
    (False, True, False, False): case1_rot_neg,     #4
    (False, True, False, True): case2_mirr,         #5
    (False, True, True, False): case4_1,            #6
    (False, True, True, True): case3,               #7
    (True, False, False, False): case1_mirr,        #8
    (True, False, False, True): case4_1_mirr,       #9
    (True, False, True, False): case2_mirr,         #10
    (True, False, True, True): case3_rot_pos,       #11
    (True, True, False, False): case2_rot_neg,      #12
    (True, True, False, True): case3_rot_neg,       #13
    (True, True, True, False): case3_mirr           #14
}


class Face:
    def __init__(self, origin, dir1, dir2, values):
        """
        A face is always oriented in the following way:

            [0,1]--[1,1]
        dir2  |      |
              |      |
            [0,0]--[1,0]
                dir1

        where the values[x,y] resides on the corresponding nodes.

        :param origin:
        :param dir1:
        :param dir2:
        :param values:
        :return:
        """
        assert type(values) is np.ndarray
        assert values.shape == (2, 2)
        assert type(origin) is np.ndarray
        assert type(dir1) is np.ndarray
        assert type(dir2) is np.ndarray

        self._origin = origin
        self._dir1 = dir1
        self._dir2 = dir2
        self._values = values

    def get_nodes(self):
        nodes = 4 * [None]
        nodes[0] = self._origin
        nodes[1] = self._origin + self._dir1
        nodes[2] = self._origin + self._dir1 + self._dir2
        nodes[3] = self._origin + self._dir2

        nodevals = [self._values[0, 0],
                    self._values[1, 0],
                    self._values[1, 1],
                    self._values[0, 1]]

        return nodes, nodevals

    def do_dualcontour(self):
        if self._values.all() or not self._values.any():
            return None, []
        else:
            key = tuple(self._values.reshape(4).tolist())
            case_handler = dc_lut[key]
            print key
            return case_handler(self._origin, self._dir1, self._dir2)

    def plot(self, ax):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
        nodes, nodevals = self.get_nodes()
        nodes = np.array(nodes)
        x = nodes[:, 0].tolist()
        y = nodes[:, 1].tolist()
        z = nodes[:, 2].tolist()
        vtx = [zip(x, y, z)]
        poly = Poly3DCollection(vtx)
        poly.set_alpha(.5)
        ax.add_collection3d(poly)

        for i in range(4):
            x = nodes[i][0]
            y = nodes[i][1]
            z = nodes[i][2]
            if nodevals[i]:
                ax.scatter(x, y, z, s=100, c='w')
            else:
                ax.scatter(x, y, z, s=20, c='k')

        dc_pts, dc_edgs = self.do_dualcontour()

        if dc_pts is not None:
            for dc_pt in dc_pts:
                x = dc_pt[0]
                y = dc_pt[1]
                z = dc_pt[2]
                ax.scatter(x, y, z, s=50, c='r')

            for dc_edg in dc_edgs:
                x = dc_pts[dc_edg,0]
                y = dc_pts[dc_edg,1]
                z = dc_pts[dc_edg,2]
                vtx = [zip(x,y,z)]
                line = Line3DCollection(vtx)
                line.set_color('k')
                ax.add_collection3d(line)

    def get_center(self):
        return self._origin + self._dir1 * .5 + self._dir2 * .5


class Cell:
    def __init__(self, origin, values, size):
        '''

        :param origin: origin of the cell. Defined as the lower front left point of the cube
        :param values: values on the cube edges. Saved in a 2x2x2 np.ndarray.
        :return:
        '''
        assert type(values) is np.ndarray
        assert values.shape == (2, 2, 2)
        self._origin = origin
        self._values = values
        self._size = size

    def get_faces(self):
        """
        when unfolding a cell, the faces are numbered in the following way: First one is the bottom face (z=0), then we
        start with the face (x=0) and go on counter-clock-wise (y=0, x=1, y=1) and finally we end at the top face.

                    f---g
                    | 4 |
            g---f---b---c---g
        y   | 5 | 1 | 0 | 3 |
        ^   h---e---a---d---h
        |           | 2 |
        --> x       e---h


        :return: list containing the faces in the described order.
        """

        faces = 6 * [None]

        h = self._size

        faces[0] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values[:, :, 0])
        faces[1] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([0, h, 0]),
                        dir2=np.array([0, 0, h]),
                        values=self._values[0, :, :])
        faces[2] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, 0, h]),
                        values=self._values[:, 0, :])
        faces[3] = Face(origin=self._origin + np.array([h, 0, 0]),
                        dir1=np.array([0, h, 0]),
                        dir2=np.array([0, 0, h]),
                        values=self._values[1, :, :])
        faces[4] = Face(origin=self._origin + np.array([0, h, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, 0, h]),
                        values=self._values[:, 1, :])
        faces[5] = Face(origin=self._origin + np.array([0, 0, h]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values[:, :, 1])

        return faces

    def get_unfold_faces(self):
        """
        when unfolding a cell, the faces are numbered in the following way: First one is the bottom face (z=0), then we
        start with the face (x=0) and go on counter-clock-wise (y=0, x=1, y=1) and finally we end at the top face.

                    f---g
                    | 4 |
            g---f---b---c---g
        y   | 5 | 1 | 0 | 3 |
        ^   h---e---a---d---h
        |           | 2 |
        --> x       e---h


        :return: list containing the faces in the described order.
        """

        faces = 6 * [None]

        h = self._size

        faces[0] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values[:, :, 0])
        faces[1] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([0, h, 0]),
                        dir2=np.array([-h, 0, 0]),
                        values=self._values[0, :, :])
        faces[2] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, -h, 0]),
                        values=self._values[:, 0, :])
        faces[3] = Face(origin=self._origin + np.array([h, 0, 0]),
                        dir1=np.array([0, h, 0]),
                        dir2=np.array([h, 0, 0]),
                        values=self._values[1, :, :])
        faces[4] = Face(origin=self._origin + np.array([0, h, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values[:, 1, :])
        faces[5] = Face(origin=self._origin + np.array([-h, 0, 0]),
                        dir1=np.array([-h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values[:, :, 1])

        return faces

    def plot(self, ax):
        faces = self.get_faces()
        for i in range(6):
            face = faces[i]
            face.plot(ax)

    def plot_unfolded(self, ax):
        faces = self.get_unfold_faces()
        for i in range(6):
            face = faces[i]
            face.plot(ax)


### test

values = np.zeros((2, 2, 2), dtype=bool)

values[0, 0, 0] = True
values[0, 1, 0] = True
#values[1, 1, 0] = True
values[1, 0, 0] = True

origin = np.array([0, 0, 0])

size = 1.0

c = Cell(origin, values, size)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
c.plot_unfolded(ax)
ax.set_aspect('equal')
