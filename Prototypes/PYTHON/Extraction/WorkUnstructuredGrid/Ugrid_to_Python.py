#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
from pylab import plot, show
import itertools as it
import cPickle
import getopt,sys
import numpy as np

# The source file: INPUT
try:
	opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
name=str(args)
file_name=name[2:len(name)-2]

# Read the source file.
reader = vtkUnstructuredGridReader()
reader.SetFileName(file_name)
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetScalarRange()


#Obtain data from the vtk file
nodes_vtk_array= reader.GetOutput().GetPoints().GetData()


#Convert to numpy array
nodes_numpy_array=vtk_to_numpy(nodes_vtk_array) 

a,b= nodes_numpy_array.shape
x,y,z=nodes_numpy_array[0:a:8,0],nodes_numpy_array[0:a:8,1],nodes_numpy_array[0:a:8,2]

cell_values=nodes_numpy_array[0:a:8]



# Dimensions 
xmin, xmax = min(x)-2, max(x)+3
ymin, ymax = min(y)-2, max(y)+3
zmin, zmax =min(z)-2, max(z)+3

print "xmin= %f" % xmin
print "xmax= %f" % xmax
print "ymin= %f" % ymin
print "ymax= %f" % ymax
print "zmin= %f" % zmin
print "zmax= %f" % zmax

dims = {'xmin': xmin,'xmax': xmax,'ymin': ymin,'ymax': ymax, 'zmin': zmin, 'zmax': zmax}

#Create Dictionary to make Search faster
newDict = {}
for point in cell_values:
    newDict[(float(point[0]), float(point[1]), float(point[2]))] = True

#Save Dictionary to further use in dc3D.py
print('Store point dictionary to binary file...')
save_file = open('Cells_03', 'wb')
cPickle.dump(newDict, save_file, -1)
save_file.close()
print('Done.\n')


#Save Dimensions
print('Store point dictionary to binary file...')
save_file = open('Dimensions_03', 'wb')
cPickle.dump(dims, save_file, -1)
save_file.close()
print('Done.\n')



################################## TESTING ########################################################################################
#1)Finding the keys
res=1
counter=0;
for i, j, k in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
	if(i,j,k) in newDict:
		counter+=1


print "Number of occupied cells = %d" % counter

#2)Assignign cube_signs
cube_verts = [np.array([x, y, z])
    for x in range(2)
    for y in range(2)
    for z in range(2)]



counter=0

for i, j, k in it.product(np.arange(dims['xmin'], dims['xmax'], res), np.arange(dims['ymin'], dims['ymax'], res), np.arange(dims['zmin'], dims['zmax'], res)):
	o = np.array([float(i), float(j), float(k)])
	cube_signs=[]	
	for v in cube_verts:
		c=True
		position = (o + v)
		key = tuple(position)
		if key in newDict:
			c=False
		cube_signs.append(c)
	if all(cube_signs) or not any(cube_signs):
        	continue
	
   
