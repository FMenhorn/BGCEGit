from dc3D import tworesolution_dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f

import numpy as np

dimensions = {'xmin': 0.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 3.5, 'zmax': 4.5}
res_fine = 1.0/4.0
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

fine_data = sample_data(doubletorus_f, resolutions['fine'], dimensions)
[verts_out_dc, quads_out_dc] = tworesolution_dual_contour(fine_data, resolutions, dimensions)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

for q in quads_out_dc['coarse']:
    vtx = verts_out_dc['coarse'][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    ax.add_collection3d(poly)

for q in quads_out_dc['fine']:
    vtx = verts_out_dc['fine'][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    #ax.add_collection3d(poly)

ax.set_xlim3d(dimensions['xmin'], dimensions['xmax'])
ax.set_ylim3d(dimensions['ymin'], dimensions['ymax'])
ax.set_zlim3d(dimensions['zmin'], dimensions['zmax'])
plt.show()

