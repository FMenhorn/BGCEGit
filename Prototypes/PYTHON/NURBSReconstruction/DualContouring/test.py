import testing.dcSample
import numpy as np
import extraction
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

__author__ = 'benjamin'

# choose example here
__EXAMPLE__ = "Path"

if __EXAMPLE__ == "Path":
    print "initializition is done later"

elif __EXAMPLE__ == "Doubletorus":
    dimensions = {'xmin': 0.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 3.0, 'zmax': 5.0}
    plot_dims = {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 5.0, 'zmin': 3.0, 'zmax': 5.0}

    res_fine = 1.0 / 8.0
    res_coarse = 1.0 / 4.0

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

    fine_data = testing.dcSample.sample_data(testing.dcSample.doubletorus_f, resolutions['fine'], dimensions)

elif __EXAMPLE__ == "Sphere":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
    plot_dims = {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}

    res_fine = 1.0 / 2.0
    res_coarse = 1.0

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

    fine_data = testing.dcSample.sample_data(testing.dcSample.sphere_f, resolutions['fine'], dimensions)

elif __EXAMPLE__ == "Torus":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
    plot_dims = {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}

    res_fine = 1.0 / 4.0
    res_coarse = 2.0

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

    fine_data = testing.dcSample.sample_data(testing.dcSample.torus_f, resolutions['fine'], dimensions)

else:
    print "Example " + __EXAMPLE__ + " not known!"
    raise Exception("ABORTING!")

if __EXAMPLE__ == "Path":
    print "Example: Path"
    path = "cantilever"
    [verts, quads, params, plot_dims, quads_objs] = extraction.extract_surface_from_path_w_plot(path)
else:
    [verts, quads, quads_objs, params] = extraction.extraction_algorithm(fine_data, resolutions, dimensions)

print "###Plotting###"

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

plane_oo = [False] * quads['coarse'].__len__()
for q in quads_objs['coarse']:
    vtx = q.vertices_plane
    vtx_orig = verts['coarse'][q.vertex_ids]
    M = vtx[1:4, :] - vtx[0, :]
    plane_oo[q.quad_id] = abs(np.linalg.det(M)) < 10 ** -10

    x = vtx[:, 0].tolist()
    y = vtx[:, 1].tolist()
    z = vtx[:, 2].tolist()
    x_orig = vtx_orig[:, 0].tolist()
    y_orig = vtx_orig[:, 1].tolist()
    z_orig = vtx_orig[:, 2].tolist()
    vtx = [zip(x, y, z)]
    vtx_orig = [zip(x_orig, y_orig, z_orig)]
    poly = Poly3DCollection(vtx_orig)
    poly.set_color('b')
    poly.set_edgecolor('k')
    # poly.set_alpha(.25)
    ax.add_collection3d(poly)

for q in quads_objs['fine']:
    vtx = verts['fine'][q]
    x = vtx[:, 0].tolist()
    y = vtx[:, 1].tolist()
    z = vtx[:, 2].tolist()
    vtx = [zip(x, y, z)]
    poly = Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

ax.set_xlim3d(plot_dims['xmin'], plot_dims['xmax'])
ax.set_ylim3d(plot_dims['ymin'], plot_dims['ymax'])
ax.set_zlim3d(plot_dims['zmin'], plot_dims['zmax'])
plt.axis('off')
plt.show()

print "###Plotting DONE###"
