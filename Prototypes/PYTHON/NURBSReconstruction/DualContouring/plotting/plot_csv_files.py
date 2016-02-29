import csv
import numpy
import DC_plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

reader=csv.reader(open("./dc_quads_coarse.csv","rb"),delimiter=';')
x=list(reader)
quads=numpy.array(x).astype('int')

reader=csv.reader(open("./dc_verts_coarse.csv","rb"),delimiter=';')
x=list(reader)
verts=numpy.array(x).astype('float')

fig = plt.figure()
ax = Axes3D(fig)

DC_plotting.plot_surface(axis=ax, quads=quads, verts=verts, color='b', alpha=.5)

fig.show()




