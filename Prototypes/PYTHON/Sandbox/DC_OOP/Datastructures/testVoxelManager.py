__author__ = 'benjamin'

import exampleData
from Dataset import Dataset2, Dataset3
from VoxelManager import VoxelManager2, VoxelManager3

ds_circl = Dataset2(exampleData.data_2D_doubletorus)

vm_circl = VoxelManager2(1.0/4.0,0,6,ds_circl)

vm_circl.calculate_dc_vertices()

vm_circl.calculate_connections()

v_verts = vm_circl.get_voxel_vertices()

import matplotlib.pyplot as plt

fig = plt.figure()

for k,vs in v_verts.items():
    for v in vs:
        p = v.get_position()
        plt.plot(p[0],p[1],'ko')

ds_circl.draw_dataset()

vm_circl.draw_voxels()

vm_circl.draw_edges()

for key, vox in vm_circl.get_voxel_dict().items():
    print str(key)+":"
    print "\t neighbor voxel at"
    print "\t"+str(vox.get_neighbor_voxels())

plt.show()

# ds_sphere = Dataset3(exampleData.data_sphere)
#
# vm_sphere = VoxelManager3(1.0/2.0,0,2,ds_sphere)
#
# vm_sphere.calculate_dc_vertices()
#
# v_verts = vm_sphere.get_voxel_vertices()
#
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.set_aspect('equal')
#
# ds_sphere.set_ax(ax)
# vm_sphere.set_ax(ax)
#
# print "###plotting###"
# print "\tplotting dc verts"
# for k,vs in v_verts.items():
#     for v in vs:
#         p = v.get_position()
#         ax.scatter(p[0],p[1],p[2],'ko')
# print "\tplotting dataset"
# #ds_sphere.draw_dataset()
# print "\tplotting voxels"
# vm_sphere.draw_voxels()
#
# ax.set_xlim3d(0,2)
# ax.set_ylim3d(0,2)
# ax.set_zlim3d(0,2)
# plt.show()

