import argparse

from BackToCAD.NURBSToSTEPAllraised import export_step
from DooSabin.DualCont_to_ABC import dooSabin_ABC
from DualContouring.extraction import extract_surface
from PetersScheme.fitting import fit_NURBS
from PetersScheme.quadvertGenerator import quad_vert_generator

# TODO: how to include INPUT: output_file_name, nonchanging_file_name

parser = argparse.ArgumentParser(description='Include path to Cells and Dimensions.')
parser.add_argument('path', type=str, help='path to Cells and Dimensions')
args = parser.parse_args()

#path="./DualContouring/cantilever/"
print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(args.path)
vertices, quads, fine_vertices = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)

print "### DooSabin ###"
A, B1, B2, C, regularPoints = dooSabin_ABC(vertices, quads)
print "### DooSabin DONE ###"

print "### Peters' Scheme ### "
NURBSMatrix, NURBSIndices = fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters)
print "### Peters' Scheme DONE### "

# TODO: nonchanging_file_name should be a zero string if not provided by the user

print "### Generating Step File ###"
export_step( NURBSIndices, NURBSMatrix, output_file_name, nonchanging_file_name)
print "### Step File DONE### "




