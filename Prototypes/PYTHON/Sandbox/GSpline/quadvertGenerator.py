__author__ = 'juan'

import numpy as np
from Vertex import Vertex
from Edge import Edge
from Quad import Quad


def quad_vert_generator():

    #_verts = np.array(np.genfromtxt('Data/Torus/torus_verts_coarse.csv', delimiter=';'))
    #_quads = np.array(np.genfromtxt('Data/Torus/torus_quads_coarse.csv', delimiter=';'))
    #_fine_verts = np.array(np.genfromtxt('Data/Torus/torus_verts_fine.csv', delimiter=';'))
    #_parameters = np.genfromtxt('Data/Torus/parameters.csv', delimiter=';')

    _verts = np.array(np.genfromtxt('Data/Torus_minimal/vers_torusminimal.csv', delimiter=';'))
    _quads = np.array(np.genfromtxt('Data/Torus_minimal/quads_torusminimal.csv', delimiter=';'))
    _fine_verts = np.array(np.genfromtxt('Data/Torus_minimal/torus_datapoints.csv', delimiter=';'))
    _parameters = np.genfromtxt('Data/Torus_minimal/parameters.csv', delimiter=';')

    # Create vertices
    vertex_list = []
    for i in range(_verts.shape[0]):
        vertex_list.append(Vertex(_id=i, _x=_verts[i, 0], _y=_verts[i, 1], _z=_verts[i, 2]))

    # Creating edges
    edge_dict = {}
    edge_id = 0
    for i in range(_quads.shape[0]):
        edges = [(_quads[i, 0], _quads[i, 1]),  # edges of this quad
                 (_quads[i, 1], _quads[i, 2]),
                 (_quads[i, 2], _quads[i, 3]),
                 (_quads[i, 3], _quads[i, 0])]
        for e in edges:
            key = tuple(sorted(e))
            if key not in edge_dict:
                edge_dict[key] = Edge(edge_id, vertex_list[int(key[0])], vertex_list[int(key[1])])
                edge_id += 1

    # Creating quads
    quad_list = []
    for i in range(_quads.shape[0]):
        a = int(_quads[i, 0])
        b = int(_quads[i, 1])
        c = int(_quads[i, 2])
        d = int(_quads[i, 3])
        e1 = tuple(sorted([_quads[i, 0], _quads[i, 1]]))  # edges of this quad
        e2 = tuple(sorted((_quads[i, 1], _quads[i, 2])))
        e3 = tuple(sorted((_quads[i, 2], _quads[i, 3])))
        e4 = tuple(sorted((_quads[i, 3], _quads[i, 0])))
        quad_list.append(Quad(i, vertex_list[a], vertex_list[b], vertex_list[c], vertex_list[d],
                             edge_dict[e1], edge_dict[e2], edge_dict[e3], edge_dict[e4]))

    # Errasing hanging nodes
    for i in range(vertex_list.__len__()):
        if not vertex_list[i].get_quads():
            vertex_list[i] = None

    # New Id's of vertices
    new_id = 0
    new_vertex_list = []
    for i in range(vertex_list.__len__()):
        if vertex_list[i] is not None:
            new_vertex_list.append(vertex_list[i])
            vertex_list[i].id = new_id
            new_id += 1

    # Check if every edge has only two quads!
    for e in edge_dict:
        if edge_dict[e].get_quads().__len__() > 2:
            print e

    # Create parameterList
    parameter_list = []
    for i in range(_parameters.shape[0]):
        parameter_list.append([quad_list[int(_parameters[i, 0])], _parameters[i, 1], _parameters[i, 2]])

    return new_vertex_list, quad_list, parameter_list, _fine_verts
















