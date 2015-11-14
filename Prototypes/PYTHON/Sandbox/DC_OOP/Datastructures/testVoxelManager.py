__author__ = 'benjamin'

import exampleData
import numpy as np
from Dataset import Dataset2, Dataset3
from VoxelManager import VoxelManager2, VoxelManager3
from Voxel import Voxel2

ds_circl = Dataset2(exampleData.data_circle, exampleData.res_circle)
ds_doubletorus = Dataset2(exampleData.data_2D_doubletorus, exampleData.res_2D_doubletorus)

vm_circl = VoxelManager2(1.0/4.0,0,2,ds_circl)
vm_doubletorus = VoxelManager2(1.0/4.0,0,6,ds_doubletorus)
vm_circl = vm_doubletorus
ds_circl = ds_doubletorus

vm_circl.calculate_dc_vertices()

# v_verts = vm_circl.get_voxel_vertices()
# v_edges = vm_circl.get_voxel_edges()

# import matplotlib.pyplot as plt
#
# fig = plt.figure()
#
# for vs in v_verts:
#     for v in vs:
#         v.draw()
#
# for e in v_edges:
#     e.draw()
#
# ds_circl.draw()
#
# vm_circl.draw_voxels()
#
# plt.show()

print "###generating data###"
print "\tdataset"
ds_sphere = Dataset3(exampleData.data_sphere, exampleData.res_sphere)
ds_doubletorus_3d = Dataset3(exampleData.data_3D_doubletorus, exampleData.res_3D_doubletorus)
print "\tvoxel manager"
vm_sphere = VoxelManager3(1.0/2.0,0,2,ds_sphere)
vm_doubletorus_3d = VoxelManager3(1.0/8.0,0,8,ds_doubletorus_3d)

vm_sphere = vm_doubletorus_3d
ds_sphere = ds_doubletorus_3d

print "###dual contouring###"
vm_sphere.calculate_dc_vertices()

print "\tcalculating vertices"
v_verts = vm_sphere.get_voxel_vertices()
print "\tgenerating quads"
v_quads = vm_sphere.get_voxel_quads()

print "###plotting###"
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

#ds_sphere.set_ax(ax)
#vm_sphere.set_ax(ax)

print "\tplotting dc verts"
for vs in v_verts:
    for v in vs:
        p = v.get_position()
        ax.scatter(p[0],p[1],p[2],'ko')
print "\tplotting dc quads"
for q in v_quads:
    vtx = []
    for v in q.get_vertices():
        vtx.append(v.get_position().tolist())
    vtx = np.array(vtx)
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    #poly.set_alpha(.25)
    ax.add_collection3d(poly)

print "\tplotting dataset"
#ds_sphere.draw_dataset()
print "\tplotting voxels"
#vm_sphere.draw_voxels()

ax.set_xlim3d(0,8)
ax.set_ylim3d(0,8)
ax.set_zlim3d(0,8)
plt.show()

