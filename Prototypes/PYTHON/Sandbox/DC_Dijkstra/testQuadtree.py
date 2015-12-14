__author__ = 'benjamin'

import numpy as np

from dc2D import dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from dcPlotting import plot_edges, plot_vertices, plot_non_manifold_vertices, plot_surface
from qtPlotting import plot_qt
from dcManifolds import detectManifolds2d
from quadtree import Quadtree
from Vertex import Vertex2
from Edge import Edge2


def transform_into_object_sets(dc_verts, dc_edges):
    vertex_set = set()
    edge_set = set()
    for v_key, v_value in dc_verts.items():
        new_vertex = Vertex2(v_value[0],v_value[1])
        vertex_set.add(new_vertex)
        dc_verts[v_key] = new_vertex

    for e in dc_edges:
        v1 = dc_verts[e[0]]
        v2 = dc_verts[e[1]]
        new_edge = Edge2(v1,v2)
        edge_set.add(new_edge)

    return vertex_set, edge_set

print "creating sample data..."
dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0}
resolution = 1.0/32.0
data = sample_data(doubletorus_f, resolution, dimensions)
print "done"

print "dual contouring..."
[dc_verts, dc_edges] = dual_contour(data, resolution, dimensions)
print "done."
#non_manifold_verts = detectManifolds2d(dc_edges)

print "transforming into objects..."
vertex_set, edge_set = transform_into_object_sets(dc_verts, dc_edges)
print "done."

print "building quadtree..."
qt = Quadtree(8.0, np.array([0,0]))
qt.add_dataset(vertex_set)
print "quadtree of depth "+str(qt.get_depth())+" constructed."
print "done."

print "plotting..."
import matplotlib.pyplot as plt

#fig = plt.figure()

#plot_qt(qt)
#plot_vertices(vertex_set)
#plot_edges(edge_set)
#plot_non_manifold_vertices(dc_verts, non_manifold_verts)

plot_qt(qt, 'b--')
plot_vertices(vertex_set,'b.')
#plot_surface(vertex_set,'b.')

qt.do_coarsening(3)
print vertex_set.__len__()
vertex_set = qt.get_dataset()
print vertex_set.__len__()

plot_qt(qt, 'r')
#plot_vertices(vertex_set,'ro')
plot_surface(vertex_set,'ro')
#plot_edges(edge_set)


plt.xlim(xmin = 0, xmax = 8)
plt.ylim(ymin = 0, ymax = 8)
plt.axis('equal')
plt.show()

