from __future__ import division

import csv

import FreeCAD
import Part
import Import
import numpy as np

"""
configuration parameters:

for the length of the knot vector, the following rule has to hold:
n_knots = n_nodes + deg + 1
n_nodes has to be chosen such that it matches with the given number of control nodes per patch in the input files
"""
input_folder = "./Torus_Fair_NURBS_AllRaised"
output_file_name = "./Torus_NURBS_AllRaised.step"
nonchanging_file_name = "./Cone.step"
plot_control_points = False

knots = [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1]
degree = 3
n_nodes = 13

# holds the faces
faceHolder = []

assert (knots.__len__() == n_nodes + degree + 1)
"""
configuration done
"""

def parse_csv_into_matrix(csv_path, out_type):
    """
    parses a csv file into a list(list(out_type))
    :param csv_path: path to the file to be parsed
    :param out_type: defines the expected type. e.g. int or float
    :return: list(list(out_type)) holding content of csv
    """
    print "Parsing file at " + csv_path + "..."
    matrix = []
    with open(csv_path) as csvfile:
        idxreader = csv.reader(csvfile, delimiter=',')
        for row in idxreader:
            new_row = []
            for idx in row:
                new_row.append(out_type(idx))
            matrix.append(new_row)
    print "File parsed."

    return matrix


def parse_all_from_folder(folder_path):
    """
    Parses a list holding all vertices and a list holding the indices of the vertices contributing to each patch from
    .csv input files. The input folder is defined above in the configuration.
    :param folder_path: path to folder holding the relevant csv fildes.
    :return: two list of vertices and vertex ids respectively
    """
    nurbs_idx = parse_csv_into_matrix(folder_path + '/NURBSPatchIndices.csv', int)
    nurbs_pts = parse_csv_into_matrix(folder_path + '/NURBSPatchPoints.csv', float)
    return nurbs_idx, nurbs_pts


def get_vertices(patch_ids, vertex_list):
    """
    Extracts the relevant vertices for a single patch from the vertex list.
    :param patch_ids: list of vertex ids of current patch
    :param vertex_list: list of all vertices
    :return: list of vertices of the current patch in lexicographical order
    """
    vertices = []
    for v_id in patch_ids:
        vertices.append(vertex_list[v_id])
    return vertices


def generate_bspline_patch(vertices):
    """
    Generates a bspine patch from the given vertices. Parameters like degree of the patch, knot vector and number of
    control points are defined above.
    :param vertices: lexicographically numbered control points in a 2D Array of 3 component points
    """
    n_nodes_u = n_nodes
    n_nodes_v = n_nodes
    degree_u = degree
    degree_v = degree
    knot_u = knots
    knot_v = knots

    patch = Part.BSplineSurface()
    patch.increaseDegree(degree_u, degree_v)

    for i in range(4, len(knot_u)-4):
        patch.insertUKnot(knot_u[i], 1, 0) # todo why is the second argument equal to 1? If anyone could explain = awesome
    for i in range(4, len(knot_v)-4):
        patch.insertVKnot(knot_v[i], 1, 0) # todo why is the second argument equal to 1? If anyone could explain = awesome

    for ii in range(0, n_nodes_u):
        for jj in range(0, n_nodes_v):
            k = ii + jj * n_nodes_u
            v = vertices[k]
            control_point = FreeCAD.Vector(v[0], v[1], v[2])
            patch.setPole(ii + 1, jj + 1, control_point, 1)
            if(plot_control_points):
                Part.show(Part.Vertex(control_point))  # plotting corresponding control points, switched on/off in configuration section
    faceHolder.append(patch.toShape()) # add to the list of Faces the patch converted to Shape


print "Creating FreeCAD Document..."
doc = FreeCAD.newDocument("tmp")
print "FreeCAD Document created."

print "Parsing input..."
nurbs_idx, nurbs_pts = parse_all_from_folder(input_folder)
print "Input files from " + input_folder + " parsed."

print "Plotting patches..."
patch_id = 0
for patch in nurbs_idx:
    print "Plotting patch no. " + str(patch_id) + "..."
    patch[:] = [x - 1 for x in patch]
    vertices = get_vertices(patch, nurbs_pts)
    generate_bspline_patch(vertices)
    patch_id += 1
print "All patches plotted."

# Create shell from face list, create solid from shell
shellHolder = Part.makeShell(faceHolder)
solidHolder = Part.makeSolid(shellHolder)

Part.show(solidHolder)

print "Exporting file..."
__objs__ = FreeCAD.getDocument("tmp").findObjects()
Import.export(__objs__, output_file_name)
print "Output file " + output_file_name + " exported."

print "Loading non-changing component..."
Import.insert(nonchanging_file_name, "tmp")

# get objects
__objs__ = []
__objs__ = FreeCAD.getDocument("tmp").findObjects()

# create fusion object
FreeCAD.getDocument("tmp").addObject("Part::MultiFuse", "FusionForBoolean")

# add objs to FusionForBoolean
FreeCAD.getDocument("tmp").FusionForBoolean.Shapes = __objs__

# compute
FreeCAD.getDocument("tmp").recompute()

print "Exporting file..."
finalWriteObjects = []
finalWriteObjects.append(FreeCAD.getDocument("tmp").getObject("FusionForBoolean"))
Import.export(finalWriteObjects, "./FusionForBoolean.step")
print "Export done."
