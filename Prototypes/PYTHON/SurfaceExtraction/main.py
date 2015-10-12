from scipy.integrate.quadpack import quad

__author__ = 'benjamin'

import dc3D
from dcSample import sample_data, sphere_f
from quad import Quad

import numpy as np

dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
res_fine = 0.5
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

fine_data = sample_data(sphere_f, resolutions['fine'], dimensions)
[verts, quads] = dc3D.tworesolution_dual_contour(fine_data, resolutions, dimensions)

verts=np.array(verts['coarse'])
quads=np.array(quads['coarse'])

quads_o = [None]*quads.shape[0]
for i in range(quads.shape[0]):
    quads_o[i]=Quad(i,quads,verts)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
ax = Axes3D(fig)

plane_oo = [False] * quads.shape[0]
for q in quads_o:
    vtx = q.compute_corner_points(verts)
    M = vtx[1:4,:]-vtx[0,:]
    plane_oo[q.id] = abs(np.linalg.det(M))<10**-10
    vtx_orig = verts[q.vertices]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    x_orig = vtx_orig[:,0].tolist()
    y_orig = vtx_orig[:,1].tolist()
    z_orig = vtx_orig[:,2].tolist()
    vtx = [zip(x,y,z)]
    vtx_orig = [zip(x_orig,y_orig,z_orig)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    ax.add_collection3d(poly)

ax.set_xlim3d(2, 6)
ax.set_ylim3d(2, 6)
ax.set_zlim3d(2, 6)
plt.show()

P=quads_o[5].compute_corner_points(verts)
np.linalg.det(P[1:4,:]-P[0,:])


