import argparse

from BackToCAD.NURBSToSTEPAllraised import export_step
from DooSabin.DualCont_to_ABC import dooSabin_ABC
from DualContouring.extraction import extract_surface
from PetersScheme.fitting import fit_NURBS
from PetersScheme.quadvertGenerator import quad_vert_generator
from DooSabin.DualCont_toABC_simple import dualCont_to_ABC_simpl

#####TESTING PATHS ######
allowed_domains_file_name = './ActiveVolumeTest/Cantilever_ToOptimize.step'
input_file_name='./ActiveVolumeTest/Cantilever.step'
path="./DualContouring/bridge"
output_file_name = "./Bridge"
fairnessWeight = 0.5
coarsening_factor = 4
nonchanging_file_name = "./ActiveVolumeTest/Cantilever_Fixed.step"
#######


print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(path, coarsening_factor)
vertices, quads, fine_vertices, new_vertex_list, edges, quad_list = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)

print "### DooSabin ###"
A, B1, B2, C, regularPoints = dualCont_to_ABC_simpl(quad_list, new_vertex_list)
print "### DooSabin DONE ###"

print "### Peters' Scheme ### "
NURBSMatrix, NURBSIndices = fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters, fairnessWeight)
print "### Peters' Scheme DONE### "

# TODO: nonchanging_file_name should be a zero string if not provided by the user

print "### Generating Step File ###"
export_step( NURBSIndices, NURBSMatrix, input_file_name, output_file_name, nonchanging_file_name, allowed_domains_file_name)
print "### Step File DONE### "




