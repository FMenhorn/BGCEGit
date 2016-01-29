import csv

import FreeCAD
import Part
import Import

def parse_csv_into_matrix(csv_path, out_type):
    matrix = []
    with open(csv_path) as csvfile:
        idxreader = csv.reader(csvfile, delimiter=';')
        for row in idxreader:
            new_row = []
            for idx in row:
                new_row.append(out_type(idx))
            matrix.append(new_row)

    return matrix


def parse_all_from_folder(folder_path):

    pts = parse_csv_into_matrix(folder_path+'/verts_coarse.csv',float)
    idx = parse_csv_into_matrix(folder_path+'/quads_coarse.csv',int)

    return pts, idx


def get_vertices(patch_ids, vertex_list):
    vertices = []
    for v_id in patch_ids:
        vertices.append(vertex_list[v_id])
    return vertices


def generate_quad(vertices):
    edges = 4 * [None]
    for i in range(4):
        edges[i] = Part.makeLine(tuple(vertices[i]),tuple(vertices[(i+1)%4]))

    wires = 4 * [None]
    wires[0] = Part.Wire([edges[0],edges[3]])
    wires[1] = Part.Wire([edges[2],edges[1]])
    wires[2] = Part.Wire([wires[0],wires[1]])
    Part.show(wires[2])

doc = FreeCAD.newDocument("tmp")
print "Document created"

pts, quads = parse_all_from_folder('./PetersSchemeInput/cantilever')
print "Stuff parsed"

for quad in quads:
    vertices = get_vertices(quad, pts)
    generate_quad(vertices)

print "points plotted"

__objs__ = FreeCAD.getDocument("tmp").findObjects()

Import.export(__objs__, "./torus_mesh.step")
print ".step exported"
