from redis.utils import dummy

__author__ = 'benjamin'

from dc2D import dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from dcPlotting import plot_edges, plot_vertices, plot_non_manifold_vertices
from dcManifolds import detectManifolds2d

dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0}
resolution = 1.0/4.0

data = sample_data(doubletorus_f, resolution, dimensions)
[dc_verts, dc_edges] = dual_contour(data, resolution, dimensions)
non_manifold_verts = detectManifolds2d(dc_edges)

import matplotlib.pyplot as plt

fig = plt.figure()

#plot_vertices(dc_verts)
plot_edges(dc_edges, dc_verts)
plot_non_manifold_vertices(dc_verts, non_manifold_verts)

plt.xlim(xmin = 0, xmax = 8)
plt.ylim(ymin = 0, ymax = 8)
plt.show()

