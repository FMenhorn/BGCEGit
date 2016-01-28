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

    pts = parse_csv_into_matrix(folder_path+'/verts_fine.csv',float)

    return pts


def generate_point(vertex):
    free_cad_vect = FreeCAD.Vector(vertex[0],vertex[1],vertex[2])
    Part.show(Part.Vertex(free_cad_vect))


doc = FreeCAD.newDocument("tmp")
print "Document created"

pts = parse_all_from_folder('./PetersSchemeInput/torus')
print "Stuff parsed"

i=0
for vertex in pts:
    i+=1
    if i % 1000 == 0:
        print i
    generate_point(vertex)

print "points plotted"

__objs__ = FreeCAD.getDocument("tmp").findObjects()

Import.export(__objs__, "./torus_pointcloud.step")
print ".step exported"
