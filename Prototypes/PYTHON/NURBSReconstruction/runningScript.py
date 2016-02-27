import argparse

from BackToCAD.NURBSToSTEPAllraised import export_step
from DooSabin.DualCont_to_ABC import dooSabin_ABC
from DualContouring.extraction import extract_surface
from PetersScheme.fitting import fit_NURBS
from PetersScheme.quadvertGenerator import quad_vert_generator



#parser = argparse.ArgumentParser(description='Include path to Cells and Dimensions.')
#parser.add_argument('path', type=str, help='path to Cells and Dimensions')
#args = parser.parse_args()

#####TESTING PATHS ######
path="./DualContouring/cantilever/"
output_file_name = "Cantilever_NURBS_AllRaised"

# file holding domain bounds (as geometry) that restrict the RAW output from Peter's scheme
allowed_domains_file_name = "./BlackWhiteCube.step"

# file holding domains that (as geometry) that need to be as they are
nonchanging_file_name = "./BackToCAD/Cone.step"
coarsening_factor = 2
fairnessWeight = 0.5
#######


print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(args.path, args.coarsening_factor)
vertices, quads, fine_vertices = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)

print "### DooSabin ###"
A, B1, B2, C, regularPoints = dooSabin_ABC(vertices, quads)
print "### DooSabin DONE ###"

print "### Peters' Scheme ### "
NURBSMatrix, NURBSIndices = fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters, args.fairnessWeight)
print "### Peters' Scheme DONE### "

# TODO: nonchanging_file_name should be a zero string if not provided by the user

print "### Generating Step File ###"
export_step( NURBSIndices, NURBSMatrix, output_file_name, nonchanging_file_name, allowed_domains_file_name)
print "### Step File DONE### "




