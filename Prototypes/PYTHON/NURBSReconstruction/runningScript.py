
import argparse

from PetersScheme.fitting import fit_NURBS
from DualContouring.extraction import extract_surface
from PetersScheme.quadvertGenerator import quad_vert_generator
from PetersScheme.DualCont_to_ABC import dooSabin_ABC


parser = argparse.ArgumentParser(description='Include path to Cells and Dimensions.')
parser.add_argument('path', type=str, help='path to Cells and Dimensions')
args = parser.parse_args()

print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(args.path)

vertices, quads, fine_vertices = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)

print "### DooSabin ###"
A, B1, B2, C, regularPoints = dooSabin_ABC(vertices, quads)
fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters)

