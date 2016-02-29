import testing.dcSample
import numpy as np
import extraction
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import dcHelpers

__author__ = 'benjamin'

# choose example here
__EXAMPLE__ = "Path"

if __EXAMPLE__ == "Path":
    print "initializition is done later"

elif __EXAMPLE__ == "Doubletorus":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}

    res_fine = 1.0 / 8.0
    res_coarse = 1.0 / 2.0

    fine_data = testing.dcSample.sample_data(testing.dcSample.doubletorus_f, res_fine, dimensions)

    fine_data, res_fine, dimensions, scaling_factor = testing.dcSample.normalize_resolution(fine_data,res_fine,dimensions)
    res_coarse = int(scaling_factor * res_coarse)

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

elif __EXAMPLE__ == "Sphere":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
    plot_dims = {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}

    res_fine = 1.0 / 4.0
    res_coarse = 1.0

    fine_data = testing.dcSample.sample_data(testing.dcSample.sphere_f, res_fine, dimensions)

    fine_data, res_fine, dimensions, scaling_factor = testing.dcSample.normalize_resolution(fine_data,res_fine,dimensions)
    res_coarse = int(scaling_factor * res_coarse)

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

elif __EXAMPLE__ == "Torus":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}

    res_fine = 1.0 / 4.0
    res_coarse = 1.0

    fine_data = testing.dcSample.sample_data(testing.dcSample.torus_f, res_fine, dimensions)

    fine_data, res_fine, dimensions, scaling_factor = testing.dcSample.normalize_resolution(fine_data,res_fine,dimensions)
    res_coarse = int(scaling_factor * res_coarse)

    resolutions = {'fine': res_fine, 'coarse': res_coarse}

else:
    print "Example " + __EXAMPLE__ + " not known!"
    raise Exception("ABORTING!")

if __EXAMPLE__ == "Path":
    print "Example: Path"
    path = "cantilever"
    coarse_scale = 4
    [verts, quads, params, dimensions, quads_objs, datasets] = extraction.extract_surface_from_path_w_plot(path, coarse_scale)
else:
    [verts, quads, quads_objs, params] = extraction.extraction_algorithm(fine_data, resolutions, dimensions)

print "###Plotting###"

nonmanifold=[]
edge_usage = dcHelpers.generate_edge_usage_dict(quads['coarse'])
for edge_identifier, used_by_quads in edge_usage.items():
    if used_by_quads.__len__() != 2:
        print used_by_quads.__len__()
        nonmanifold.append(edge_identifier)

print nonmanifold
for e in nonmanifold:
    print e[0]
    print verts['coarse'][e[0]]
    print e[1]
    print verts['coarse'][e[1]]

fig = plt.figure()
ax = Axes3D(fig)

#datasets['fine'].plot(ax,'r',1)
#datasets['coarse'].plot(ax,'b',.25)

#plane_oo = [False] * quads['coarse'].__len__()

for q in quads['coarse']:
    if None in q.tolist():
        continue
    q = np.array(q,dtype=int)
    vtx_orig = verts['coarse'][q]

    x_orig = vtx_orig[:, 0].tolist()
    y_orig = vtx_orig[:, 1].tolist()
    z_orig = vtx_orig[:, 2].tolist()
    vtx_orig = [zip(x_orig, y_orig, z_orig)]
    poly = Poly3DCollection(vtx_orig)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

for nonmanifold_edge in nonmanifold:
    vtx = verts['coarse'][list(nonmanifold_edge)]
    x = vtx[:, 0].tolist()
    y = vtx[:, 1].tolist()
    z = vtx[:, 2].tolist()
    vtx = [zip(x, y, z)]
    line = Line3DCollection(vtx)
    line.set_color('r')
    line.set_linewidth(5)
    ax.add_collection3d(line)
'''
for q in quads['coarse']:

    vtx = verts['coarse'][q]
    x = vtx[:, 0].tolist()
    y = vtx[:, 1].tolist()
    z = vtx[:, 2].tolist()
    vtx = [zip(x, y, z)]
    poly = Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.5)
    ax.add_collection3d(poly)
'''
x_mean = (dimensions['xmax']-dimensions['xmin'])/2.0
y_mean = (dimensions['ymax']-dimensions['ymin'])/2.0
z_mean = (dimensions['zmax']-dimensions['zmin'])/2.0

x_min = dimensions['xmin']
y_min = dimensions['ymin']
z_min = dimensions['zmin']
minmin = min([x_min, y_min, z_min])

x_max = dimensions['xmax']
y_max = dimensions['ymax']
z_max = dimensions['zmax']
maxmax = max([x_max, y_max, z_max])

width = maxmax-minmin

ax.set_xlim3d(x_mean-width*.5, x_mean+width*.5)
ax.set_ylim3d(y_mean-width*.5, y_mean+width*.5)
ax.set_zlim3d(z_mean-width*.5, z_mean+width*.5)
ax.set_aspect('equal')
plt.show()

print "###Plotting DONE###"
