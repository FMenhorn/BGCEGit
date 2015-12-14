__author__ = 'benjamin'

import matplotlib.pyplot as plt

def plot_edges(edges):
    for e in edges:
        v = e.get_vertices()
        pos1 = v[0].get_position()
        pos2 = v[1].get_position()
        x = [pos1[0], pos2[0]]
        y = [pos1[1], pos2[1]]
        plt.plot(x, y, 'b')


def plot_vertices(vertices,opt):
    for v in vertices:
        pos = v.get_position()
        x = pos[0]
        y = pos[1]
        plt.plot(x, y,opt)


def plot_surface(vertices, opt):
    for v in vertices:
        pos = v.get_position()
        x = pos[0]
        y = pos[1]
        plt.plot(x, y,opt)
        for e in v.get_edges():
            v_c = e.get_vertices()
            pos1 = v_c[0].get_position()
            pos2 = v_c[1].get_position()
            x = [pos1[0], pos2[0]]
            y = [pos1[1], pos2[1]]
            plt.plot(x, y, 'k')


def plot_non_manifold_vertices(dc_verts, non_manifold_verts):
    for non_manifold_vert_key in non_manifold_verts:
        v = dc_verts[non_manifold_vert_key]
        x = v[0]
        y = v[1]
        plt.plot(x,y,'xr')


def plot_quad_tree(quadtree):
    raise Exception("TO BE IMPLEMENTED!")
