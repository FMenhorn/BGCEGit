# from __future__ import division
from operator import pos

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools as it


class ManifoldEdge:
    def __init__(self, _manifold_edge_key, _manifold_edge_quads, _manifold_edge_vertex_quads, _dc_vindex, _dataset, _resolution):
        self.resolution = _resolution
        self.v_key = [None] * 2
        for i in range(2):
            self.v_key[i] = search_vertex_key_from_index(_dc_vindex, _manifold_edge_key[i])

        self.edge_dir, self.edge_dim = self.calculate_edge_dir(_manifold_edge_key, _dc_vindex)
        self.neighbour_keys, self.neighbour_directions = self.calculate_neighbour_keys()
        self.middle_value_key, self.middle_plane_index = self.calculate_middle_value_key()
        self.middle_sign = self.calculate_middle_sign(_dataset)   #CHANGED
        self.manifold_edge_quads = _manifold_edge_quads
        self.manifold_edge_vertex_quads = _manifold_edge_vertex_quads

    def calculate_middle_sign(self,_dataset):
         key=self.middle_value_key    #middle_value _key is a tuple
         if key in _dataset:
                return True
         else:
             return False


    def calculate_edge_dir(self, _manifold_edge_key, _dc_vindex):
        import numpy as np
        v_o = [None] * 2
        #v_o describes the origin of the respective voxel
        for i in range(2):
            v_o[i] = np.array(self.v_key[i])

        edge_dir = v_o[1] - v_o[0]
        edge_dir = np.abs(edge_dir)/np.linalg.norm(edge_dir)
        edge_dim = np.where(edge_dir == 1)[0][0]

        return edge_dir, edge_dim

    def calculate_middle_value_key(self):
        import numpy as np

        displacement = np.array([1.0,1.0,1.0]) * self.resolution / 2
        displacement[self.edge_dim] = 0.0
        if self.v_key[0][self.edge_dim] > self.v_key[1][self.edge_dim]: # v_key[0] is in the plane crossed by the edge
            middle_plane_idx = 0
            return tuple(np.array(self.v_key[0]) + displacement), middle_plane_idx
        else: # v_key[1] is in that plane
            middle_plane_idx = 1
            return tuple(np.array(self.v_key[1]) + displacement), middle_plane_idx

    def calculate_neighbour_keys(self):
        import numpy as np

        neighbor_directions = []

        for d in range(3):
            if d != self.edge_dim:
                for j in [-1,1]:
                    neighbor_direction = np.zeros(3)
                    neighbor_direction[d] = j
                    neighbor_directions.append(neighbor_direction)

        neighbor_keys = 2*[4*[None]]
        for i in range(2):
            for j in range(4):
                neighbor_keys[i][j] = tuple(np.array(self.v_key[i])+self.resolution*neighbor_directions[j])

        return neighbor_keys, neighbor_directions

    def resolve(self, _dataset, _vindex, _dc_quads):
        new_quads = []
        delete_quads = self.manifold_edge_quads

        i = self.middle_plane_index
        for n1,n2 in [(0,2),(0,3),(1,2),(1,3)]: # create new quads and remove manifold quads
            sign_direction = np.array(self.neighbour_directions[n1])+np.array(self.neighbour_directions[n2])
            sign_key = tuple(np.array(self.middle_value_key)+self.resolution*.5*sign_direction)
            #sign = _dataset[sign_key] > 0   #CHANGED
            sign=False
            key=sign_key    #middle_value _key is a tuple
            if key in _dataset:
                sign= True

            if sign != self.middle_sign:
                new_quad = [None] * 4
                new_quad[0] = _vindex[tuple(np.array(self.v_key[0]) + self.resolution*self.neighbour_directions[n1])]
                new_quad[1] = _vindex[tuple(np.array(self.v_key[1]) + self.resolution*self.neighbour_directions[n1])]
                new_quad[2] = _vindex[tuple(np.array(self.v_key[1]) + self.resolution*self.neighbour_directions[n2])]
                new_quad[3] = _vindex[tuple(np.array(self.v_key[0]) + self.resolution*self.neighbour_directions[n2])]
                new_quads.append(new_quad)

        # change remaining references to removed edge
        change_quads = []
        for i in self.manifold_edge_vertex_quads:
            change_quads.append(np.array(_dc_quads[i]))

        for i in range(change_quads.__len__()):
            for j in range(i+1,change_quads.__len__()):
                same_vertex = np.intersect1d(change_quads[i],change_quads[j])
                if same_vertex.__len__() == 1:
                    i1 = np.where(change_quads[i] == same_vertex)[0][0]
                    i2 = np.where(change_quads[j] == same_vertex)[0][0]

                    change_quads[i][i1] = change_quads[j][(i2+1)%4]
                    change_quads[j][i2] = change_quads[i][(i1+1)%4]

        new_quads += change_quads
        delete_quads += self.manifold_edge_vertex_quads

        return new_quads, delete_quads


#DUAL CONTOURING

dirs = [np.array([0.0,0.0,1.0]), np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0])]

# Vertices of cube
cube_verts = [np.array([x, y, z])
    for x in range(2)
    for y in range(2)
    for z in range(2)]

# Edges of cube
cube_edges = [
    [k for (k,v) in enumerate(cube_verts) if v[i] == a and v[j] == b]
    for a in range(2)
    for b in range(2)
    for i in range(3)
    for j in range(3) if i != j]


# Use non-linear root finding to compute intersection point
def estimate_hermite(data, v0, v1):
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    return x0


def tworesolution_dual_contour(dataset, resolutions, dims):
    [dc_verts_fine,dc_quads_fine]=dual_contour(dataset,
                                               resolutions['fine'],
                                               dims,
                                               coarse_level = False)
    [dc_verts_coarse,dc_quads_coarse]=dual_contour(dataset,
                                                   resolutions['coarse'],
                                                   dims,
                                                   coarse_level = True)

    dc_verts={'fine': dc_verts_fine,'coarse': dc_verts_coarse}
    dc_quads={'fine': dc_quads_fine,'coarse': dc_quads_coarse}

    return dc_verts, dc_quads


# Input:
# data = voxel data
# res = resolution
# dims = dimension of data
def dual_contour(data, res, dims, coarse_level):
    # Compute vertices
    dc_verts = []
    vindex = {}
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
        o = np.array([float(x), float(y), float(z)])

        cube_signs=[]
        # Get signs for cube
        for v in cube_verts:
            position = (o + v*res)
            key = tuple(position)
            c=True
            if key in data:
                c=False
            cube_signs.append(c)

        if all(cube_signs) or not any(cube_signs):
            continue

        # Estimate hermite data
        h_data = []
        for e in cube_edges:
            if cube_signs[e[0]] != cube_signs[e[1]]:
                h_data.append(estimate_hermite(data, o + cube_verts[e[0]]*res, o + cube_verts[e[1]]*res))

        counter = 0
        v = np.array([0.0, 0.0, 0.0])

        for p in h_data:
            v += np.array(p)
            counter += 1

        v /= 1.0 * counter

        # Throw out failed solutions
        if la.norm(v - o) > 2 * res:
            continue

        # Emit one vertex per every cube that crosses
        vindex[tuple(o)] = len(dc_verts)
        dc_verts.append(v)

    # Construct faces
    dc_quads = []
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
        if not (x, y, z) in vindex:
            continue

        # Emit one edge per each edge that crosses
        o = np.array([float(x), float(y), float(z)])
        for i in range(3):
            for j in range(i):
                if tuple(o + res*dirs[i]) in vindex and tuple(o + res*dirs[j]) in vindex and tuple(o + res*(dirs[i] + dirs[j])) in vindex:
                    k = 3-(i+j) # normal id
                    c=True
                    d=True
                    if tuple(o+res*dirs[i]+res*dirs[j]) in data:
                        c=False
                    if tuple(o+res*dirs[i]+res*dirs[j]+res*dirs[k]) in data:
                        d=False
                    #if (data[tuple(o+res*dirs[i]+res*dirs[j])] > 0) != (data[tuple(o+res*dirs[i]+res*dirs[j]+res*dirs[k])] > 0): # dir[i]+dir[j]+dir[k] = [1,1,1] for all!
                    if c != d:
                        dc_quads.append([vindex[tuple(o)], vindex[tuple(o+res*dirs[i])], vindex[tuple(o+res*dirs[i]+res*dirs[j])], vindex[tuple(o+res*dirs[j])]])

    if coarse_level:
        dc_quads = resolve_manifold_edges(dc_verts, vindex, dc_quads, data, res)


    return np.array(dc_verts), np.array(dc_quads)


def create_manifold_edges(_dc_quads, _dc_vindex, _dataset, _resolution):

    edge_usage_list = {}

    for i in range(_dc_quads.__len__()):
        q = _dc_quads[i]
        edges = [(q[0],q[1]),
                 (q[1],q[2]),
                 (q[2],q[3]),
                 (q[3],q[0])]

        edge_keys=[]
        for e in edges:
            key = tuple(sorted(e))
            edge_keys.append(key)

        for e in edge_keys:
            if e in edge_usage_list:
                edge_usage_list[e].append(i)
            else:
                edge_usage_list[e] = [i]


    manifold_edges = {}

    for e_u in edge_usage_list:
        if edge_usage_list[e_u].__len__() > 2:
            vertex_usage_list = []
            for v in e_u:
                for q_idx in range(_dc_quads.__len__()):
                    q = _dc_quads[q_idx]
                    if (v in q) and (q_idx not in edge_usage_list[e_u]):
                        vertex_usage_list.append(q_idx)

            manifold_edges[e_u]=ManifoldEdge(e_u, edge_usage_list[e_u], vertex_usage_list, _dc_vindex, _dataset, _resolution)

    return manifold_edges


def resolve_manifold_edges(_dc_verts, _dc_vindex, _dc_quads, _data, _resolution):
    manifold_edges = create_manifold_edges(_dc_quads, _dc_vindex, _data, _resolution)
    new_quads_list = []
    delete_quads_list = []

    for manifold_edge_key, manifold_edge in manifold_edges.items():
        new_quads, delete_quads = manifold_edge.resolve(_data, _dc_vindex, _dc_quads)
        new_quads_list += new_quads
        delete_quads_list += delete_quads

    _dc_quads = update_quad_list(_dc_quads, new_quads_list, delete_quads_list)

    return _dc_quads


def search_vertex_key_from_index(_dc_vindex, idx):
    for key in _dc_vindex:
        if int(_dc_vindex[key]) == int(idx):
            return key

    print "ERROR! INDEX %d not found" % idx
    quit()


def update_quad_list(_dc_quads, new_quads_list, delete_quads_list):
    for i in delete_quads_list:
        _dc_quads[i] = None
    while None in _dc_quads:
        _dc_quads.remove(None)
    _dc_quads += new_quads_list
    return _dc_quads
