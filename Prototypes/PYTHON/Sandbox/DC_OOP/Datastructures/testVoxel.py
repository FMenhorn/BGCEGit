__author__ = 'benjamin'

import numpy as np

from Voxel import Voxel2, Voxel3
from Dataset import Dataset
import exampleData

ds2 = Dataset(exampleData.data2)
ds3 = Dataset(exampleData.data3)

vox2 = Voxel2(np.array([0,0]),1,ds2)

vox3 = Voxel3(np.array([0,0,0]),1,ds3)