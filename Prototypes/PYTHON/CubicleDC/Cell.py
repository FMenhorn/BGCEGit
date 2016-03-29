import numpy as np
from rotation import rotation_around_pt
from dc_lut import dc_lut

face_edge_connectivity = [
    [{'edge':3,'face':2},  # connectivity of face 0
     {'edge':1,'face':3},
     {'edge':2,'face':4},
     {'edge':0,'face':1}],
    [{'edge':3,'face':0},  # connectivity of face 1
     {'edge':1,'face':4},
     {'edge':2,'face':5},
     {'edge':0,'face':2}],
    [{'edge':3,'face':1},  # connectivity of face 2
     {'edge':1,'face':5},
     {'edge':2,'face':3},
     {'edge':0,'face':0}],
    [{'edge':3,'face':4},  # connectivity of face 3
     {'edge':1,'face':0},
     {'edge':2,'face':2},
     {'edge':0,'face':5}],
    [{'edge':3,'face':5},  # connectivity of face 4
     {'edge':1,'face':1},
     {'edge':2,'face':0},
     {'edge':0,'face':3}],
    [{'edge':3,'face':3},  # connectivity of face 5
     {'edge':1,'face':2},
     {'edge':2,'face':1},
     {'edge':0,'face':4}]
]

face_edge_uid = {(0, 0): 0,
                 (2, 3): 0,
                 (0, 1): 1,
                 (3, 1): 1,
                 (0, 2): 2,
                 (4, 2): 2,
                 (0, 3): 3,
                 (1, 0): 3,
                 (5, 0): 4,
                 (3, 3): 4,
                 (5, 1): 5,
                 (2, 1): 5,
                 (5, 2): 6,
                 (1, 2): 6,
                 (5, 3): 7,
                 (4, 0): 7,
                 (1, 1): 8,
                 (4, 1): 8,
                 (2, 0): 9,
                 (1, 3): 9,
                 (2, 2): 10,
                 (3, 2): 10,
                 (3, 0): 11,
                 (4, 3): 11
                 }

class Face:
    def __init__(self, origin, dir1, dir2, values, face_id):
        """
        :param origin:
        :param dir1:
        :param dir2:
        :param values:
        :param face_id:
        :return:
        """
        assert type(origin) is np.ndarray
        assert type(dir1) is np.ndarray
        assert type(dir2) is np.ndarray

        self._origin = origin
        self._dir1 = dir1
        self._dir2 = dir2
        self._values = values
        self._face_id = face_id

    def get_local_values(self):
        """
        A face is always oriented in the following way:

             [3]----[2]
        dir2  |      |
              |      |
             [0]----[1]
                dir1

        where the local_values[i,j] resides on the corresponding nodes.
        :return: 4 array holding the local values in the local indexing
        """
        nodes = self.get_nodes()

        local_values = [self._values[tuple(nodes[0])],
                        self._values[tuple(nodes[1])],
                        self._values[tuple(nodes[2])],
                        self._values[tuple(nodes[3])]]

        return local_values

    def get_nodes(self):
        """
        A face is always oriented in the following way:

             [3]----[2]
        dir2  |      |
              |      |
             [0]----[1]
                dir1

        where the nodes[i,j] refers to the global coordinates of each node from the local system.
        :return: 2x2 array holding the global coordinates of the nodes in the local indexing
        """

        nodes = [self._origin,
                 self._origin + self._dir1,
                 self._origin + self._dir1 + self._dir2,
                 self._origin + self._dir2]

        return nodes

    def do_dualcontour(self):
        if np.array(self.get_local_values()).all() or not np.array(self.get_local_values()).any():
            return None, [], []
        else:
            key = tuple(self.get_local_values())
            case_handler = dc_lut[key]
            return case_handler(self._origin, self._dir1, self._dir2)

    def plot(self, ax):
        self._plot_plane(ax, [0, 0, 0], [0, 0, 0])
        self._plot_values(ax, [0, 0, 0], [0, 0, 0])
        self._plot_dc(ax, [0,0,0], [0,0,0])

    def plot_unfolded(self, ax):
        if self._face_id == 0:
            translation = [0, 0, 0]
            rotation = [0, 0, 0]
        elif self._face_id == 1:
            translation = [0, 0, 0]
            rotation = [0, -.5 * np.pi, 0]
        elif self._face_id == 2:
            translation = [0, 0, 0]
            rotation = [.5*np.pi, 0, 0]
        elif self._face_id == 3:
            translation = self._dir1 - np.cross(self._dir1/np.linalg.norm(self._dir1),self._dir2)
            rotation = [0, .5*np.pi, 0]
        elif self._face_id == 4:
            translation = self._dir2 - np.cross(self._dir1/np.linalg.norm(self._dir1),self._dir2)
            rotation = [-.5*np.pi, 0, 0]
        elif self._face_id == 5:
            translation = 3*self._dir1 + np.cross(self._dir1/np.linalg.norm(self._dir1),self._dir2)
            rotation = [np.pi, 0, 0]
        else:
            translation = [0, 0, 0]
            rotation = [0, 0, 0]

        self._plot_plane(ax, translation, rotation)
        self._plot_values(ax, translation, rotation)
        self._plot_dc(ax, translation, rotation)

    def _plot_plane(self, ax, translation, rotation):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        nodes = self.get_nodes()
        nodes = np.array(nodes)
        x = []
        y = []
        z = []
        for node in nodes:
            node = rotation_around_pt(node, self._origin, rotation)
            x.append(node[0] + translation[0])
            y.append(node[1] + translation[1])
            z.append(node[2] + translation[2])
        vtx = [zip(x, y, z)]
        poly = Poly3DCollection(vtx)
        poly.set_alpha(.5)
        ax.add_collection3d(poly)

    def _plot_values(self, ax, translation, rotation):
        nodes = self.get_nodes()
        nodes = np.array(nodes)
        for i in range(4):
            node = nodes[i, :]
            x, y, z = rotation_around_pt(node, self._origin, rotation) + translation
            node_key = tuple(nodes[i, :])
            if self._values[node_key]:
                ax.scatter(x, y, z, s=100, c='w')
            else:
                ax.scatter(x, y, z, s=20, c='k')

    def _plot_dc(self, ax, translation, rotation):
        from mpl_toolkits.mplot3d.art3d import Line3DCollection
        dc_pts, dc_edgs, dc_face_edge = self.do_dualcontour()

        if dc_pts is not None:
            for dc_pt in dc_pts:
                x,y,z = rotation_around_pt(dc_pt, self._origin, rotation) + translation
                ax.scatter(x, y, z, s=50, c='r')


            for dc_edg in dc_edgs:
                nodes = dc_pts[dc_edg, :]
                x = []
                y = []
                z = []
                for node in nodes:
                    node = rotation_around_pt(node, self._origin, rotation)
                    x.append(node[0] + translation[0])
                    y.append(node[1] + translation[1])
                    z.append(node[2] + translation[2])
                vtx = [zip(x, y, z)]
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

        self._values = dict()
        self._values[tuple(origin)] = values[0, 0, 0]
        self._values[tuple(origin + [size, 0, 0])] = values[1, 0, 0]
        self._values[tuple(origin + [0, size, 0])] = values[0, 1, 0]
        self._values[tuple(origin + [0, 0, size])] = values[0, 0, 1]
        self._values[tuple(origin + [size, size, 0])] = values[1, 1, 0]
        self._values[tuple(origin + [size, 0, size])] = values[1, 0, 1]
        self._values[tuple(origin + [0, size, size])] = values[0, 1, 1]
        self._values[tuple(origin + [size, size, size])] = values[1, 1, 1]

        self._origin = origin
        self._size = size

    def get_faces(self):
        """
        when unfolding a cell, the faces are numbered in the following way: First one is the bottom face (z=0), then we
        start with the face (x=0) and go on counter-clock-wise (y=0, x=1, y=1) and finally we end at the top face.

                    h---g
                    | 4 |
            g---h---d---c---g
        y   | 5 | 1 | 0 | 3 |
        ^   f---e---a---b---f
        |           | 2 |
        --> x       e---f


        :return: list containing the faces in the described order.
        """

        faces = 6 * [None]

        h = self._size

        faces[0] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([h, 0, 0]),
                        dir2=np.array([0, h, 0]),
                        values=self._values,
                        face_id=0)
        faces[1] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([0, h, 0]),
                        dir2=np.array([0, 0, h]),
                        values=self._values,
                        face_id=1)
        faces[2] = Face(origin=self._origin + np.array([0, 0, 0]),
                        dir1=np.array([0, 0, h]),
                        dir2=np.array([h, 0, 0]),
                        values=self._values,
                        face_id=2)
        faces[3] = Face(origin=self._origin + np.array([h, h, h]),
                        dir1=np.array([0, 0, -h]),
                        dir2=np.array([0, -h, 0]),
                        values=self._values,
                        face_id=3)
        faces[4] = Face(origin=self._origin + np.array([h, h, h]),
                        dir1=np.array([-h, 0, 0]),
                        dir2=np.array([0, 0, -h]),
                        values=self._values,
                        face_id=4)
        faces[5] = Face(origin=self._origin + np.array([h, h, h]),
                        dir1=np.array([0, -h, 0]),
                        dir2=np.array([-h, 0, 0]),
                        values=self._values,
                        face_id=5)

        return faces

    def plot(self, ax):
        faces = self.get_faces()
        dc_vtx = {}
        dc_edg = set()
        face_vtx = 6 * [None]
        face_edg = 6 * [None]
        face_vtx_on_edg = 6 * [None]

        additional_id = 12
        all_ids = dict(face_edge_uid)
        for i in range(6):
            print "face %d"%(i)
            face = faces[i]
            face.plot(ax)
            local_dc_vtx, local_dc_edg, vtx_on_edg = face.do_dualcontour()
            print vtx_on_edg

            for j in range(vtx_on_edg.__len__()):
                v = local_dc_vtx[j,:]
                i_edge = vtx_on_edg[j]
                key = (i,i_edge)
                if i_edge < 4:
                    dc_vtx[all_ids[key]] = v
                else:
                    dc_vtx[additional_id] = v
                    all_ids[key] = additional_id
                    additional_id += 1

            for e in local_dc_edg:
                key0 = all_ids[(i,vtx_on_edg[e[0]])]
                key1 = all_ids[(i,vtx_on_edg[e[1]])]
                dc_edg.add((key0,key1))

        print dc_vtx
        print dc_edg

        # build ring

        ring = []
        ring += list(dc_edg.pop())
        print ring
        while dc_edg.__len__() != 0:
            for s in dc_edg:
                if ring[-1] in s:
                    id = int(not s.index(ring[-1]))
                    ring.append(s[id])
                    to_be_removed = s
                    break
            dc_edg.remove(to_be_removed)

        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        x = []
        y = []
        z = []
        for id in ring:
            node = dc_vtx[id]
            x.append(node[0])
            y.append(node[1])
            z.append(node[2])
        vtx = [zip(x, y, z)]
        poly = Poly3DCollection(vtx)
        poly.set_alpha(1)
        poly.set_color('r')
        ax.add_collection3d(poly)




    def plot_unfolded(self, ax):
        faces = self.get_faces()
        for i in range(6):
            face = faces[i]
            face.plot_unfolded(ax)


### test

values = np.zeros((2, 2, 2), dtype=bool)

testcase = 7

if testcase == 1:
    # case 1
    values[0,0,0] = True
elif testcase == 2:
    # case 2
    values[1,0,0] = True
elif testcase == 3:
    # case 3
    values[0,0,0] = True
    values[1,0,0] = True
elif testcase == 4:
    # case 4
    values[1,1,0] = True
elif testcase == 51:
    # case 5_1
    values[0,0,0] = True
    values[1,1,0] = True
elif testcase == 52:
    # case 5_2
    values[1,0,0] = True
    values[0,1,0] = True
elif testcase == 6:
    # case 6
    values[1,0,0] = True
    values[1,1,0] = True
elif testcase == 7:
    # case 7
    values[0,0,0] = True
    values[1,0,0] = True
    values[1,1,0] = True
else:
    raise Exception()

# remaining cases 8-14 from symmetry!

origin = np.array([0, 0, 0])

size = 1.0

c = Cell(origin, values, size)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
#c.plot_unfolded(ax)
c.plot(ax)
ax.set_aspect('equal')
ax.set_xlim3d(0, 1)
ax.set_ylim3d(0,1)
ax.set_zlim3d(0,1)
