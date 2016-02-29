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

dimensions = {'xmin':-170,'xmax':195,'ymin':100,'ymax':340,'zmin':-30,'zmax':120}

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




