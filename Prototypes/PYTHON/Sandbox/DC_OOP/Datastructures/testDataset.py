__author__ = 'benjamin'

import numpy as np
import matplotlib.pyplot as plt

import exampleData
from Dataset import Dataset2, Dataset3



# test case for these classes:
pos1 = exampleData.pos1
pos2 = exampleData.pos2
pos3 = (1.0, 1.0)
pos4 = (1.0, 3.0)

data2 = exampleData.data2
ds2 = Dataset2(data2)

dp = ds2.get_datapoint_at(pos1)
assert (dp.get_position() == np.array(pos1)).all()
assert dp.get_value() == True
dp = ds2.get_datapoint_at(np.array(pos1))
dp.get_position()
assert (dp.get_position() == np.array(pos1)).all()
assert dp.get_value() == True

dp = ds2.get_datapoint_at(pos2)
assert (dp.get_position() == np.array(pos2)).all()
assert dp.get_value() == False

dp = ds2.get_datapoint_at(pos4)
assert dp is None

assert ds2.get_num_datapoints() == 2
assert ds2.add_datapoint(pos1,True) == False
assert ds2.get_num_datapoints() == 2
assert ds2.add_datapoint(pos3,True) == True
assert ds2.get_num_datapoints() == 3

ds2.add_datapoint((0,0), False)
ds2.add_datapoint((0,1), True)
ds2.add_datapoint((1,0), False)

data3 = exampleData.data3
ds3 = Dataset3(data3)

ds2.draw()

plt.show()
