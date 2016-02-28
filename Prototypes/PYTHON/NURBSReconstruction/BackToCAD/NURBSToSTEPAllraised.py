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

    return patch.toShape()


def export_step(nurbs_idx, nurbs_pts, input_file_name, output_file_name, nonchanging_file_name, allowed_domains_file_name):
#def export_step(nurbs_idx, nurbs_pts, output_file_name, nonchanging_file_name):

    knots = [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1]
    degree = 3
    n_nodes = 13

    # holds the faces
    faceHolder = []

    assert (knots.__len__() == n_nodes + degree + 1)



    print "Creating FreeCAD Document..."
    doc = FreeCAD.newDocument("tmp")
    print "FreeCAD Document created."

    #print "Parsing input..."
    #nurbs_idx, nurbs_pts = parse_all_from_folder(input_folder)
    #print "Input files from " + input_folder + " parsed."

    print "Plotting patches..."
    patch_id = 0
    for patch in nurbs_idx:
        print "Plotting patch no. " + str(patch_id) + "..."
        vertices = get_vertices(patch, nurbs_pts)
        new_patch = generate_bspline_patch(vertices, n_nodes, degree, knots)
        faceHolder.append(new_patch) # add to the list of Faces the patch converted to Shape
        patch_id += 1
    print "All patches plotted."

    # Create shell from face list, create solid from shell
    shellHolder = Part.makeShell(faceHolder)
    solidHolder = Part.makeSolid(shellHolder)

    Part.show(solidHolder)

    print "Exporting RAW file..."
    __objs__ = FreeCAD.getDocument("tmp").findObjects()
    Import.export(__objs__, output_file_name+"_RAW.step")
    print "Output file " + output_file_name+"_RAW.step" + " exported."

#    for obj in __objs__:
#        FreeCAD.getDocument("tmp").removeObject(obj.Name)

#    Import.insert("./"+output_file_name, "tmp")

    if len(allowed_domains_file_name) != 0:
        print "Checking allowed domains..."
        # take the intersection of allowed domains
        # read in step file for allowed domains
        Import.insert(allowed_domains_file_name, "tmp")
        __objs__ = FreeCAD.getDocument("tmp").findObjects()

        # - take intersection of each allowed domain with original Peter's output 
        # - store as separate "Common" object
        # - delete loaded allowed domains
        for i in range(1, len(__objs__)):
            FreeCAD.getDocument("tmp").addObject("Part::MultiCommon", "Common"+str(i))
            FreeCAD.getDocument("tmp").findObjects()[-1].Shapes = [__objs__[0], __objs__[i]]
            FreeCAD.getDocument("tmp").recompute()
            FreeCAD.getDocument("tmp").removeObject(__objs__[i].Name)

        # update __objs__
        __objs__ = FreeCAD.getDocument("tmp").findObjects()

        if len(__objs__) > 2:
            # create a fuse object and union all "Common"s
            FreeCAD.getDocument("tmp").addObject("Part::MultiFuse", "Fuse")
            FreeCAD.getDocument("tmp").Fuse.Shapes = __objs__[1: len(__objs__)]
            print FreeCAD.getDocument("tmp").Fuse.Shapes
            FreeCAD.getDocument("tmp").recompute()

            # remove "Commons"s
            for i in range(0, len(__objs__)):
                FreeCAD.getDocument("tmp").removeObject(__objs__[i].Name)

        # update __objs__
        __objs__ = FreeCAD.getDocument("tmp").findObjects()

        # remove Peter's original version
        FreeCAD.getDocument("tmp").removeObject(__objs__[0].Name)

        print "Exporting ALLOWED file..."
        __objs__ = FreeCAD.getDocument("tmp").findObjects()
        Import.export(__objs__, output_file_name+"_ALLOWED.step")
        print "Output file " + output_file_name+"_ALLOWED.step" + " exported."

    if len(nonchanging_file_name) != 0:
        print "Loading non-changing component..."
        Import.insert(nonchanging_file_name, "tmp")

        # get objects
        __objs__ = FreeCAD.getDocument("tmp").findObjects()

        # create fusion object
        FreeCAD.getDocument("tmp").addObject("Part::MultiFuse", "FusionTool")

        # add objs to FusionTool
        FreeCAD.getDocument("tmp").FusionTool.Shapes = __objs__[0: len(__objs__)]

        # compute
        FreeCAD.getDocument("tmp").recompute()

        print "Exporting BOOLEANED file..."
        __objs__.append(FreeCAD.getDocument("tmp").getObject("FusionTool"))
        Import.export(__objs__, output_file_name+"_BOOLEANED.step")
        print "Output file " + output_file_name+"_BOOLEANED.step" + " exported."

    print "Export done."
