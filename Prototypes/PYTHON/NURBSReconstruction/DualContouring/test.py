import testing.dcSample
import numpy as np
import extraction
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import dcHelpers

def plot_surface(axis, quads, verts, color, alpha):
    for q in quads:
        vtx = verts[q]
        x = vtx[:, 0].tolist()
        y = vtx[:, 1].tolist()
        z = vtx[:, 2].tolist()
        vtx = [zip(x, y, z)]
        poly = Poly3DCollection(vtx)
        poly.set_color(color)
        poly.set_edgecolor('k')
        poly.set_alpha(alpha)
        axis.add_collection3d(poly)

def plot_hairs(axis, quads_objs, verts, params, color):
    lines_data = []
    points_data_x = []
    points_data_y = []
    points_data_z = []
    for i in range(verts.__len__()):
        q_id = int(params[i][0])
        q = quads_objs[q_id]
        v = verts[i]
        base_v, d = q.projection_onto_plane(v)

        lines_data.append([v.tolist(),base_v.tolist()])
        points_data_x.append(v[0])
        points_data_y.append(v[1])
        points_data_z.append(v[2])
    line = Line3DCollection(lines_data)
    line.color(color)
    axis.add_collection3d(line)
    #axis.scatter(points_data_x, points_data_y, points_data_z,color='k')


__author__ = 'benjamin der Starke'

# choose example here
__EXAMPLE__ = "Torus"

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

    res_fine = 1.0 / 2.0
    res_coarse = 2.0

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
    coarse_scale = 8
    [verts, quads, params, dimensions, quads_objs, datasets] = extraction.extract_surface_from_path_w_plot(path, coarse_scale)
else:
    [verts, quads, quads_objs, params, datasets] = extraction.extraction_algorithm(fine_data, resolutions, dimensions)

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

#datasets['fine'].plot(axis=ax,color='r',alpha=1)
#datasets['coarse'].plot(axis=ax,color='k',alpha=0)

plot_surface(axis=ax, quads=quads['coarse'], verts=verts['coarse'], color='b', alpha=.5)
#plot_surface(axis=ax, quads=quads['fine'], verts=verts['fine'], color='r', alpha=.5)

plot_hairs(axis=ax, quads_objs=quads_objs['coarse'], verts=verts['fine'], params=params, color='k')

for nonmanifold_edge in nonmanifold:
    vtx = verts['coarse'][list(nonmanifold_edge)]
    x = vtx[:, 0].tolist()
    y = vtx[:, 1].tolist()
    z = vtx[:, 2].tolist()
    vtx = [zip(x, y, z)]
    line = Line3DCollection(vtx)
    line.set_color('r')
    line.set_linewidth(5)
    #ax.add_collection3d(line)

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
