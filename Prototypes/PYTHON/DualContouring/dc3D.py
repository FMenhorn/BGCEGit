#from __future__ import division

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools as it

#Cardinal directions
from skimage.morphology.selem import cube

dirs_norm = [ [1,0,0], [0,1,0], [0,0,1] ]

#Vertices of cube
cube_verts_norm = [ np.array([x, y, z])
    for x in range(2)
    for y in range(2)
    for z in range(2) ]

#Edges of cube
cube_edges = [ 
    [ k for (k,v) in enumerate(cube_verts_norm) if v[i] == a and v[j] == b ]
    for a in range(2)
    for b in range(2)
    for i in range(3) 
    for j in range(3) if i != j ]

#Use non-linear root finding to compute intersection point
def estimate_hermite(f, df, v0, v1):
    t0 = .5#opt.brentq(lambda t : f((1.-t)*v0 + t*v1), 0, 1)
    x0 = (1.-t0)*v0 + t0*v1
    return (x0, df(x0))

#Input:
# f = implicit function
# df = gradient of f
# nc = resolution bullshit...
# res = resolution
def dual_contour(f, df, nc, res):
    dirs = (res*np.array(dirs_norm)).tolist()
    cube_verts = (res*np.array(cube_verts_norm)).tolist()
    #Compute vertices
    dc_verts = []
    vindex   = {}
    for x,y,z in it.product(range(int(nc/res)), range(int(nc/res)), range(int(nc/res))):
        o = np.array([x,y,z])
        o_res = o*res

        #Get signs for cube
        cube_signs = [ f(o_res+v)>0 for v in cube_verts ]

        if all(cube_signs) or not any(cube_signs):
            continue

        #Estimate hermite data
        h_data = [ estimate_hermite(f, df, o_res+cube_verts[e[0]], o_res+cube_verts[e[1]])
            for e in cube_edges if cube_signs[e[0]] != cube_signs[e[1]] ]

        #Solve qef to get vertex
        #A = [ n for p,n in h_data ]
        #b = [ np.dot(p,n) for p,n in h_data ]
        #v, residue, rank, s = la.lstsq(A, b)

        counter = 0
        v = np.array([0.0,0.0,0.0])
        #print "Start accu"
        for p,n in h_data:
            #print p
            v += np.array(p)
            counter+=1

        # print "Before:"
        # print v
        v /= 1.0*counter
        # print "After:"
        # print v

        #print "A="+ str(A) + "\n"

        #Throw out failed solutions
        if la.norm(v-o_res) > 2*res:
            continue

        # if o_res[0]-int(o_res[0]) is not 0:
        #     print "JUHU!"
        #     print cube_signs
        #     print v
        #     print o_res
        # else:
        #     print "NO JUHU!"
        #     print v
        #     print o_res

        #Emit one vertex per every cube that crosses
        vindex[ tuple(o) ] = len(dc_verts)
        dc_verts.append(v)

    #Construct faces
    dc_faces = []
    for x,y,z in it.product(range(int(nc/res)), range(int(nc/res)), range(int(nc/res))):
        if not (x,y,z) in vindex:
            continue

        #Emit one face per each edge that crosses
        o = np.array([x,y,z])
        for i in range(3):
            for j in range(i):
                if tuple(o + dirs_norm[i]) in vindex and tuple(o + dirs_norm[j]) in vindex and tuple(o + dirs_norm[i] + dirs_norm[j]) in vindex:
                    #dc_faces.append( [vindex[tuple(o)], vindex[tuple(o+dirs[i])], vindex[tuple(o+dirs[j])]] )
                    #dc_faces.append( [vindex[tuple(o+dirs[i]+dirs[j])], vindex[tuple(o+dirs[j])], vindex[tuple(o+dirs[i])]] )
                    dc_faces.append( [vindex[tuple(o)], vindex[tuple(o+dirs_norm[i])],vindex[tuple(o+dirs_norm[i]+dirs_norm[j])], vindex[tuple(o+dirs_norm[j])]] )

    return dc_verts, dc_faces

#import mayavi.mlab as mlab

center = np.array([16.0,16.0,16.0])
radius = 10.0

def test_f(x):
    d = x-center
    return np.dot(d,d) - radius**2

def test_df(x):
    d = x-center
    return d / np.sqrt(np.dot(d,d))

n = 32
res = 1

[verts, quads] = dual_contour(test_f, test_df, n, res)

import csv

with open('vertsMATLAB.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for v in verts:
        csvwriter.writerow(v)

with open('quadsMATLAB.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for q in quads:
        csvwriter.writerow(np.array(q)+1)
# mlab.triangular_mesh(
#             [ v[0] for v in verts ],
#             [ v[1] for v in verts ],
#             [ v[2] for v in verts ],
#             tris)
