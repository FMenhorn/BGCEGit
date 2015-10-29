__author__ = 'benjamin'

import exampleData
from Dataset import Dataset
from VoxelManager import VoxelManager2

ds2 = Dataset(exampleData.data2)

vm2 = VoxelManager2(.5,0,1,ds2)
