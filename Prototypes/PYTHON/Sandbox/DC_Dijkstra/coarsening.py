__author__ = 'benjamin'

import numpy as np
import networkx as nx
from Vertex import Vertex2
from Edge import Edge2


def coarsen(vertex_set):
    connected_sets = find_connected_sets(vertex_set)

    coarsened_vertex_set = set()

    for connected_set in connected_sets:
        collapsed_vertex = collapse_vertices(connected_set)
        coarsened_vertex_set.add(collapsed_vertex)

    return coarsened_vertex_set


def collapse_vertices(vertex_set):
    position_collapsed_vertex = np.zeros(2)
    n_vertices = 0
    for v in vertex_set: # calculate mean position
        position_collapsed_vertex += v.get_position()
        n_vertices += 1
    position_collapsed_vertex /= n_vertices
    # generate new vertex
    collapsed_vertex = Vertex2(position_collapsed_vertex[0], position_collapsed_vertex[1])

    # redraw connections of edges connected to old vertices to new vertex
    print "redraw edges of set:"
    print vertex_set
    for v in vertex_set:
        print "\tvertex"+str(v)+":"
        candidate_edges = v.get_edges() # all edges are candidates
        print "\thas edges"+str(candidate_edges)
        for e in candidate_edges: # traverse all edges of the vertex set
            print "\t\tedge:"+str(e)
            for i in range(2):
                e_vtx = e.get_vertices()[i]
                if e_vtx in vertex_set:
                    print "\t\t\tredrawing: "+str(e.get_vertices()[i])+"  @  "+str(collapsed_vertex)
                    e.change_vertex(i,collapsed_vertex)
                    collapsed_vertex.add_edge(e)

    return collapsed_vertex


def find_connected_vertices(vertex_set):
    print "connected vertices of "+str(vertex_set)
    connected_vertices_set = set()
    for v in vertex_set:
        print "\t" + str(v) + ":"
        connected_to_v = v.get_directly_connected_vertices()
        print "\t" + str(connected_to_v)
        for v_to_v in connected_to_v:
            if v_to_v not in vertex_set:
                print "adding "+str(v_to_v)
                connected_vertices_set.add(v_to_v)

    return connected_vertices_set


def find_connected_sets(vertex_set):
    connected_sets = set()
    added_vertices = list()
    vertex_list = list(vertex_set)

    C = setup_connectivity_matrix(vertex_list)

    print C

    G = nx.Graph(C) # create Graph from matrix
    sp = nx.shortest_path(G) # find all shortest paths

    print connected_sets
    for source, targets in sp.items():
        if source not in added_vertices:
            added_vertices += list(targets)
            connected_set = set()
            for t in targets:
                connected_set.add(vertex_list[t])
            print connected_set
            connected_sets.add(frozenset(connected_set))

    return connected_sets


def setup_connectivity_matrix(vertex_list):
    N = vertex_list.__len__()
    C = np.zeros([N,N])

    for i in range(N):
        C[i,i] = 0
        base_v = vertex_list[i]
        connected_vertices = base_v.get_directly_connected_vertices()

        for j in range(N):
            conn_v = vertex_list[j]
            if conn_v in connected_vertices:
                C[i,j] = 1

    return C