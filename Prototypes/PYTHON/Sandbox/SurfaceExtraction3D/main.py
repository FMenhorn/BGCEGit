__author__ = 'benjamin'

from dc3D import tworesolution_dual_contour
from dcSample import sample_data, sphere_f, doubletorus_f, torus_f
from quad import Quad
from dcHelpers import export_as_csv

import cPickle
import numpy as np


def transform_dict(cellsDict):
    dataset = {}
    for key in cellsDict:
        dataset[key] = -1

    return dataset


def refine(verts, quads):
    verts_refined = list(verts.tolist())
    for q in quads:
        centroid = np.zeros(3)
        for v_id in q:
            centroid += np.array(verts[v_id])

        centroid /= 4
        verts_refined.append(centroid.tolist())

        for v_id in q:
            verts_refined.append(((centroid + np.array(verts[v_id]))/2).tolist())

    return verts_refined


def find_closest_quads(_point, _quadlist, _n_closest):
    d_sq_list = [None] * _quadlist.__len__() # empty list for distances point to all quads
    for i in range(_quadlist.__len__()): # iterate over all quads
        d_sq = _quadlist[i].measure_centroid_distance_squared(_point) # distance to centroid
        d_sq_list[i] = d_sq

    idx_list = sorted(range(len(d_sq_list)), key=lambda k: d_sq_list[k])
    n_closest_idx = idx_list[:_n_closest]

    return n_closest_idx

#choose example here
__EXAMPLE__ = "Doubletorus"

if __EXAMPLE__ == "Cantilever":
    wfFile = open('Cantilever/Cells_01', 'rb')
    cellsDict = cPickle.load(wfFile)
    wfFile.close()

    wfFile = open('Cantilever/Dimensions_01', 'rb')
    dimensions = cPickle.load(wfFile)
    wfFile.close()

    res_fine = 1.0
    res_coarse = res_fine * 2.0

    resolutions = {'fine': res_fine,'coarse': res_coarse}

    fine_data = transform_dict(cellsDict)

    plot_dims =  {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}
    plot_dims = dimensions

elif __EXAMPLE__ == "Doubletorus":
    dimensions = {'xmin': 4.0, 'xmax': 6.0, 'ymin': 3.0, 'ymax': 5.0, 'zmin': 3.0, 'zmax': 5.0}
    plot_dims =  {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 5.0, 'zmin': 3.0, 'zmax': 5.0}

    res_fine = 1.0/8.0
    res_coarse = 1.0/4.0

    resolutions = {'fine': res_fine,'coarse': res_coarse}

    fine_data = sample_data(doubletorus_f, resolutions['fine'], dimensions)

elif __EXAMPLE__ == "Sphere":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
    plot_dims =  {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}

    res_fine = 1.0/2.0
    res_coarse = 1.0

    resolutions = {'fine': res_fine,'coarse': res_coarse}

    fine_data = sample_data(sphere_f, resolutions['fine'], dimensions)

elif __EXAMPLE__ == "Torus":
    dimensions = {'xmin': 0.0, 'xmax': 8.0, 'ymin': 0.0, 'ymax': 8.0, 'zmin': 0.0, 'zmax': 8.0}
    plot_dims =  {'xmin': 2.0, 'xmax': 6.0, 'ymin': 2.0, 'ymax': 6.0, 'zmin': 2.0, 'zmax': 6.0}

    res_fine = 1.0/4.0
    res_coarse = 2.0

    resolutions = {'fine': res_fine,'coarse': res_coarse}

    fine_data = sample_data(torus_f, resolutions['fine'], dimensions)

else:
    print "Example "+__EXAMPLE__+" not known!"
    raise Exception("ABOTRING!")

print "###Dual Contouring###"
print "..."
[verts_out_dc, quads_out_dc, manifolds] = tworesolution_dual_contour(fine_data, resolutions, dimensions)
print "###Dual Contouring DONE###"

N_quads = {'coarse': quads_out_dc['coarse'].__len__(), 'fine': quads_out_dc['fine'].__len__()}
N_verts = {'coarse': verts_out_dc['coarse'].__len__(), 'fine': verts_out_dc['fine'].__len__()}

quads = {'coarse': [None] * N_quads['coarse'], 'fine': [None] * N_quads['fine']}
verts = {'coarse': verts_out_dc['coarse'], 'fine': verts_out_dc['fine']} # todo substitute with vertex objects

for i in range(N_quads['coarse']):
    quads['coarse'][i]=Quad(i,quads_out_dc['coarse'],verts_out_dc['coarse'])

print "###Projecting Datapoints onto coarse quads###"

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

# # do projection of fine verts on coarse quads
# N_closest_candidates = 4 # compute list of N_closest_candidates closest quads
# param = []
#
# verts_refined=refine(verts['fine'], quads_out_dc['fine'])
# #for vertex in verts_refined:
# for vertex in verts['fine']:
#     closest_idx_candidates = find_closest_quads(vertex, quads['coarse'], N_closest_candidates) # find N closest quads with fast criterion: distance to centroid
#
#     distance_min = np.inf
#     for candidate_idx in closest_idx_candidates: # iterate over all candidates from coarse criterion
#         projected_point, distance, u, v = \
#             quads['coarse'][candidate_idx].projection_onto_quad(vertex) # find closest quad with fine criterion: projection onto quad
#
#         if abs(distance) < distance_min:
#             projected_point_min = projected_point
#             distance_min = abs(distance)
#             u_min = u
#             v_min = v
#             idx_min = candidate_idx
#
#         #only plotting information
#         start = projected_point_min
#         end = vertex
#         x = [start[0],end[0]]
#         y = [start[1],end[1]]
#         z = [start[2],end[2]]
#         vtx = [zip(x,y,z)]
#         line = Line3DCollection(vtx)
#         line.set_color('k')
#         line.set_linewidth(.5)
#
#         #ax.scatter(end[0],end[1],end[2],'bo')
#         #ax.scatter(start[0],start[1],start[2],'ro')
#
#         #ax.add_collection3d(line)
#
#
#     param.append(np.array([idx_min,u_min,v_min]))
#
# param = np.array(param)

print "###Projecting Datapoints onto coarse quads DONE###"

print "###Exporting output###"
export_as_csv(verts_out_dc['coarse'],'verts_coarse')
#export_as_csv(verts_refined,'verts_fine')
export_as_csv(quads_out_dc['coarse'],'quads_coarse')
export_as_csv(quads_out_dc['fine'],'quads_fine')
#export_as_csv(param,'param')
print "###Exporting output DONE###"

print "###Plotting###"

cool_edge = None

for key, edge in manifolds['coarse'].items():
    if edge.v_kind[0] is "outside" and edge.v_kind[1] is "outside":
    	if cool_edge is None:
		print edge.v_idx
		cool_edge = list(edge.v_idx)
		cool_edge += edge.v_children_idx[0]
		cool_edge += edge.v_children_idx[1]
		print cool_edge
    if cool_edge is not None and any([idx in edge.v_idx for idx in cool_edge]):
	    vtx = verts['coarse'][list(edge.v_idx)]
	    x = vtx[:,0].tolist()
	    y = vtx[:,1].tolist()
	    z = vtx[:,2].tolist()
	    vtx = [zip(x,y,z)]
	    edge = Line3DCollection(vtx)
	    edge.set_color('r')
	    edge.set_linewidth(5.0)
	    ax.add_collection3d(edge)

plane_oo = [False] * quads['coarse'].__len__()
for q in quads['coarse']:
    if any([idx in q.vertex_ids for idx in cool_edge]):
        vtx = q.vertices_plane
        vtx_orig = verts['coarse'][q.vertex_ids]
        M = vtx[1:4,:]-vtx[0,:]
        plane_oo[q.quad_id] = abs(np.linalg.det(M))<10**-10

        x = vtx[:,0].tolist()
        y = vtx[:,1].tolist()
        z = vtx[:,2].tolist()
        x_orig = vtx_orig[:,0].tolist()
        y_orig = vtx_orig[:,1].tolist()
        z_orig = vtx_orig[:,2].tolist()
        vtx = [zip(x,y,z)]
        vtx_orig = [zip(x_orig,y_orig,z_orig)]
        poly=Poly3DCollection(vtx_orig)
        poly.set_color('b')
        poly.set_edgecolor('k')
        poly.set_alpha(.5)
        ax.add_collection3d(poly)

for q in quads_out_dc['fine']:
    vtx = verts['fine'][q]
    x = vtx[:,0].tolist()
    y = vtx[:,1].tolist()
    z = vtx[:,2].tolist()
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('r')
    poly.set_edgecolor('k')
    poly.set_alpha(.25)
    #ax.add_collection3d(poly)


#ax.set_xlim3d(plot_dims['xmin'], plot_dims['xmax'])
#ax.set_ylim3d(plot_dims['ymin'], plot_dims['ymax'])
#ax.set_zlim3d(plot_dims['zmin'], plot_dims['zmax'])
ax.set_xlim3d(4.5,5.1)
ax.set_ylim3d(4.4,5)
ax.set_zlim3d(3.8,4.2)
plt.axis('off')
plt.show()

print "###Plotting DONE###"




