__author__ = 'benjamin'

import numpy as np
import matplotlib.pyplot as plt

from Voxel import Voxel2, Voxel3
from Dataset import Dataset2, Dataset3
import exampleData

ds2 = Dataset2(exampleData.data2)
ds3 = Dataset3(exampleData.data3)
ds_circ = Dataset2(exampleData.data_circle)

print ds_circ

ds2.add_datapoint((0, 0),True)

vox2 = Voxel2(np.array([0,0]),1,ds2)

print ds2.get_all_dataset_values()
print vox2.get_signs()
print vox2.get_signs()

print vox2._get_sign_change_edges()
print vox2._get_roots_sign_change_edges()

vox3 = Voxel3(np.array([0,0,0]),1,ds3)
print vox3.get_signs()

print ds_circ.get_all_dataset_values()

vox4 = Voxel2(np.array([0,0]),.1,ds_circ)

print vox2
print vox4

print vox4.get_origin()
print vox2.get_signs()
print vox4.get_signs()
print vox4._get_sign_change_edges()
print vox4._get_roots_sign_change_edges()
print vox4.generate_dc_vertices()
print vox4._dc_vertices
print vox4.get_origin()
for i in range(4):
    print vox4.neighbor_keys_of_edge(i)

vox2.draw()
plt.show()