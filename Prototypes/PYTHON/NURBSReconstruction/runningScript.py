import scipy.io as sio
import numpy as np
import scipy.sparse as sp
import argparse

from writeMatrices import *
from leastSquares import solve_least_squares_problem
from createFairnessControlMeshCoefs import createFairnessControlMeshCoefs
from createGlobalControlMeshCoefs import createGlobalControlMeshCoefs
from quadvertGenerator import quad_vert_generator
from sortAB1B2VIndices import sortAB1B2VIndices
from scaleAwayParameters import scaleAwayParameters
from DualCont_to_ABC import dooSabin_ABC

parser = argparse.ArgumentParser(description='Include path to Cells and Dimensions.')
parser.add_argument('path', type=str, help='path to Cells and Dimensions')
args = parser.parse_args()

print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(args.path)

vertices, quads, fine_vertices = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)

print "### DooSabin ###"
A, B1, B2, C, regularPoints = dooSabin_ABC(vertices, quads)

print "### Preprocessing ###"
# Throw away any datapoints which are NaN or outside the parameter range [0,1]
# since these cause trouble. (+ Scale the resulting ones so that max and min
# param values are 1 and 0 repspectively in both u and v)

[parameters, fine_vertices] = scaleAwayParameters(parameters, fine_vertices)
[newA, newB1, newB2, newC] = sortAB1B2VIndices(A, B1, B2, C)
print "Done."

print "Calculating coefs."
coefs = createGlobalControlMeshCoefs(parameters, quads, newA, newB1, newB2, newC, regularPoints)
print "Done."
print "Calculating fair coefs."
fair_coefs = createFairnessControlMeshCoefs(quads, newA, newB1, newB2, newC, regularPoints)
print "fair_coefs.shape = "+str(fair_coefs.shape)
print "Done."

print "Sparsify..."
sparse_coefs = sp.csr_matrix(coefs)
sparse_fair_coefs = sp.csr_matrix(fair_coefs)
print "Done."

print "Concatenating matrices."
fairnessWeight = 2.0
joined_verts = sp.vstack([scipy.array(fine_vertices), scipy.zeros([fair_coefs.shape[0], 3])]).todense()
joined_coefs = sp.vstack([sparse_coefs, fairnessWeight * sparse_fair_coefs])
print "Done."

print "Least squares..."
vertices = solve_least_squares_problem(joined_coefs, joined_verts)
print "Done."
write_matrix_to_csv(vertices,'vertices.csv')
write_matrix_to_asc(vertices,'vertices.asc')

#plotBezierSurfaceWhole(quads, newA, newB1, newB2, newC, regularPoints, vertices)

#[biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
#csvwrite('biquadraticPatchIndices.csv',biqIndices);
#csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
#csvwrite('bicubicPatchIndices.csv',bicIndices);

#[NURBSMatrix,NURBSIndices] = createNURBSMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('NURBSPatchPoints.csv',NURBSMatrix);
#csvwrite('NURBSPatchIndices.csv',NURBSIndices);
