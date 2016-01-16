from __future__ import division

import csv

import FreeCAD
import Part
import Import
import numpy as np


def sample_patch(N_nodes):
    x0 = 1.0
    y0 = 1.0
    z0 = 0.0
    h = .1
    nurbs_pts = N_nodes * N_nodes * [None]
    patch = []

    id = 0
    for i in range(N_nodes):
        for j in range(N_nodes):
            x = x0 + i * h
            y = y0 + j * h
            z = x0 + i**2 * h
            nurbs_pts[i+N_nodes*j]=[x,y,z]
            id = id + 1
            patch.append(id)

    return [patch], nurbs_pts


def parse_csv_into_matrix(csv_path, out_type):
    print "parsing file at "+csv_path
    matrix = []
    with open(csv_path) as csvfile:
        idxreader = csv.reader(csvfile, delimiter=',')
        for row in idxreader:
            new_row = []
            for idx in row:
                new_row.append(out_type(idx))
            matrix.append(new_row)

    return matrix


def parse_all_from_folder(folder_path):

    nurbs_idx = parse_csv_into_matrix(folder_path+'/NURBSPatchIndices.csv',int)
    nurbs_pts = parse_csv_into_matrix(folder_path+'/NURBSPatchPoints.csv',float)

    return nurbs_idx, nurbs_pts


def get_vertices(patch_ids, vertex_list):
    vertices = []
    for v_id in patch_ids:
        v_id = v_id - 1 # MATLAB indexing -> PYTHON indexing!!!
        vertices.append(vertex_list[v_id])
    return vertices


def generate_bspline_patch(vertices, n_nodes_u, n_nodes_v):
    def knot_uniform(deg, n_nodes):
        n_knots = n_nodes + deg + 1
        knots = np.zeros(n_knots)

        for i in range(deg):
            knots[i] = 0
        for i in range(n_nodes):
            knots[i+deg] = (i) / (n_nodes-deg)
        for i in range(deg):
            knots[-i-1] = 1

        return knots.tolist()

    degree_u = 1
    degree_v = 1
    #knot_u = [0, 0, 0, 0, .25, 0.25, 0.25, 0.5, 0.5, .5, 0.75, 0.75, .75, 1, 1, 1, 1]
    #knot_v = [0, 0, 0, 0, .25, 0.25, 0.25, 0.5, 0.5, .5, 0.75, 0.75, .75, 1, 1, 1, 1]
    knot_u = knot_uniform(degree_u, n_nodes_u)
    knot_v = knot_uniform(degree_v, n_nodes_v)
    #[0,0,0,0,0.25,0.25,0.25,0.5,0.5,0.75,0.75,0.75,1,1,1,1]
    #knot_u=[0,0,0,.5,1,1,1]
    #knot_v=[0,0,0,.5,1,1,1]

    patch = Part.BSplineSurface()
    patch.increaseDegree(degree_u, degree_v)

    id = 1
    for i in range(0, len(knot_u)):  # -1):
        patch.insertUKnot(knot_u[i], id, 0.0000001)
    id = 1
    for i in range(0, len(knot_v)):  # -1):
        patch.insertVKnot(knot_v[i], id, 0.0000001)

    for ii in range(0, n_nodes_u):
        for jj in range(0, n_nodes_v):
            k = ii+jj*n_nodes_u
            v = vertices[k]
            control_point = FreeCAD.Vector(v[0],v[1],v[2])
            patch.setPole(ii+1,jj+1,control_point, 1)
            #Part.show(Part.Vertex(control_point))

    Part.show(patch.toShape())


doc = FreeCAD.newDocument("tmp")
print "Document created"

nurbs_idx, nurbs_pts = parse_all_from_folder('./TorusFairNURBS')
print "Stuff parsed"

N_nodes = 11

# uncomment for plotting sample patch
#nurbs_idx, nurbs_pts = sample_patch(N_nodes)
#

# uncomment for plotting only one of many patches
#nurbs_idx = [nurbs_idx[0]]
#

for patch in nurbs_idx:
    vertices = get_vertices(patch, nurbs_pts)
    generate_bspline_patch(vertices, N_nodes, N_nodes)

__objs__ = FreeCAD.getDocument("tmp").findObjects()

Import.export(__objs__, "./FairTorusNURBS.step")
print ".step exported"



