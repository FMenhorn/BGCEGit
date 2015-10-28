__author__ = 'benjamin'

from dc2D import tworesolution_dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from dcHelpers import gradient_from_data

import numpy as np

dimensions = {'xmin': 0.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0}
res_fine = 1.0/8.0
res_coarse = res_fine * 2.0
resolutions = {'fine': res_fine,'coarse': res_coarse}

fine_data = sample_data(doubletorus_f, resolutions['fine'], dimensions)
fine_gdata = gradient_from_data(fine_data, resolutions['fine'])
[verts_out_dc, quads_out_dc] = tworesolution_dual_contour(fine_data, fine_gdata, resolutions, dimensions)


import matplotlib.pyplot as plt

fig = plt.figure()

for q in quads_out_dc['fine']:
    vtx = verts_out_dc['fine'][q]
    x = vtx[:,0]
    y = vtx[:,1]
    #plt.plot(x, y, 'b')
    #plt.plot(x, y, 'bo')

for q in quads_out_dc['coarse']:
    vtx = verts_out_dc['coarse'][q]
    x = vtx[:,0]
    y = vtx[:,1]
    plt.plot(x, y, 'k')
    plt.plot(x, y,'ko')
''' # useful for debugging
for v in manifold_verts_out_dc['coarse']:
    x = v.x
    y = v.y
    plt.plot(x, y,'kx')
'''
for key in fine_data:
    if (key[0] % res_fine == 0) and (key[1] % res_fine == 0):
        if fine_data[key] > 0: # outer point
            plt.plot(key[0],key[1],'b.')
        elif fine_data[key] < 0: # inner point
            plt.plot(key[0],key[1],'r.')
    if (key[0] % res_coarse == 0) and (key[1] % res_coarse == 0):
        if fine_data[key] > 0: # outer point
            plt.plot(key[0],key[1],'bx')
        elif fine_data[key] < 0: # inner point
            plt.plot(key[0],key[1],'rx')

for key in fine_gdata:
    dx = fine_gdata[key][0]
    dy = fine_gdata[key][1]
    if dx != 0 or dy != 0:
        l = np.sqrt(dx**2 + dy**2)
        dx /= l
        dy /= l
        #Q = plt.quiver(key[0],key[1],dx*res_fine,dy*res_fine,width = .0005, headwidth = 2, headlength = 2)

plt.grid(True)
plt.xlim(xmin = -1, xmax = 7)
plt.ylim(ymin = 1 , ymax = 7)
plt.show()

