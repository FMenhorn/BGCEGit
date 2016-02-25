from __future__ import division

import sys

FREECADPATH = '/usr/lib/freecad/lib'
sys.path.append(FREECADPATH)

import FreeCAD
import Part
import Import

PLOT_CONTROL_POINTS = False

def get_vertices(patch_ids, vertex_list):
        """
        Extracts the relevant vertices for a single patch from the vertex list.
        :param patch_ids: list of vertex ids of current patch
        :param vertex_list: list of all vertices
        :return: list of vertices of the current patch in lexicographical order
        """
        vertices = []
        for v_id in patch_ids:
            v_id = v_id - 1  # MATLAB indexing -> PYTHON indexing!!!
            vertices.append(vertex_list[v_id])
        return vertices


def generate_bspline_patch(vertices, n_nodes, degree, knots):
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
            if(PLOT_CONTROL_POINTS):
                Part.show(Part.Vertex(control_point))  # plotting corresponding control points, switched on/off in configuration section
    Part.show(patch.toShape())  # plots the patch


def export_step(output_file_name, nurbs_indices, control_points):
    """
    exports our internal nurbs data format to a step file with nurbs patches
    :param output_file_name:
    :param nurbs_indices:
    :param control_points:
    :return:
    """

    # configuration parameters:
    # for the length of the knot vector, the following rule has to hold:
    # n_knots = n_nodes + deg + 1
    # n_nodes has to be chosen such that it matches with the given number of control nodes per patch in the input files

    knots = [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1]
    degree = 3
    n_nodes = 13
    assert (knots.__len__() == n_nodes + degree + 1)

    # configuration done

    print "Creating FreeCAD Document..."
    doc = FreeCAD.newDocument("tmp")
    print "FreeCAD Document created."

    print "Plotting patches..."
    patch_id = 0
    for nurbs_patch in nurbs_indices:
        print "Plotting patch no. " + str(patch_id) + "..."
        vertices = get_vertices(nurbs_patch, control_points)
        generate_bspline_patch(vertices, n_nodes, degree, knots)
        patch_id += 1
    print "All patches plotted."

    print "Exporting file..."
    __objs__ = FreeCAD.getDocument("tmp").findObjects()
    Import.export(__objs__, output_file_name)
    print "Output file " + output_file_name + " exported."