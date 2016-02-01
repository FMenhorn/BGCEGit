import scipy.io as sio
import numpy as np
import scipy
import scipy.sparse as sp
import scipy.sparse.linalg as lin
import csv

from createFairnessControlMeshCoefs import createFairnessControlMeshCoefs
from quadvertGenerator import quad_vert_generator
from helper_functions import get_num_edges_meeting
from createBicubicCoefMatrices import createBicubicCoefMatrices
from createLocalParamsExtraordinary import createLocalParamsExtraordinary
from get3x3ControlPointIndexMask import get3x3ControlPointIndexMask
from getBezierPointCoefs import getBezierPointCoefs
from getBicubicBezierPointCoefs import getBicubicBezierPointCoefs
from getExtraOrdCornerIndexMask import getExtraOrdCornerIndexMask
from sortAB1B2VIndices import sortAB1B2VIndices
from scaleAwayParameters import scaleAwayParameters


vertices, quads, fine_vertices = quad_vert_generator()

# For now we use test data to not run Annas slow code
#dc_to_peter(vertex_list, quad_list)


def write_matrix_to_csv(matrix, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            csvwriter.writerow(row[:])

def write_tensor3_to_csv(tensor, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in tensor:
            csvwriter.writerow(row.T.flatten())


def read_matrix_from_csv(filename):
    matrix = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            matrix.append(row)
    return scipy.array(matrix)


def createGlobalControlMeshCoefs(parameterCoordinates, quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                     quad_control_point_indices):
    """
    Takes, for N datapoints, an array parameterCoordinates[Nx3](for every
    datapoint: first entry the quad index, second and third parameterson a patch that spans over [0,1]x[0,1]
    for the quad. The function computes the coefficient matrix for between
    each datapoint and the array of M/16 quads x [4x4] vertex control points,
    outputting the coefficients as an N x M matrix.
    """

    N = parameterCoordinates.shape[0]
    M = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1]
    coefsMatrix = np.zeros((N,M))

    """
    Precalculate the coefficients between all the vertex control points and
    the bezier control points for 7 different number of intersecting
    edges as a start

    (number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
    first coord, bezier point second coord)
    """

    #extraOrdinaryCoefsRaw = np.zeros((7,4,7,4,4))
    ACoefsRaw = np.zeros((7,7,4,4))
    B1CoefsRaw = np.zeros((7,7,4,4))
    B2CoefsRaw = np.zeros((7,7,4,4))
    CCoefsRaw  = np.zeros((7,7,4,4))

    for num_quads in range(3,8):
        [ACoefsRaw[num_quads-1, 0:num_quads, :, :],
         B1CoefsRaw[num_quads-1, 0:num_quads, :, :],
         B2CoefsRaw[num_quads-1, 0:num_quads, :, :],
         CCoefsRaw[num_quads-1, 0:num_quads, :, :]] = createBicubicCoefMatrices(num_quads) # compared to matlab by Saumi & Benni -> VALID

    coefsRawTemp = np.zeros((4,7,4,4))

    print "Main Loop Coeffs"
    for p in range(N):
        if p%100 == 0:
            print "processing point %d of %d..." % (p, N)
        #check if on a corner patch : if both coords are outside [0.25,0.75]
        quadParameters = parameterCoordinates[p, 1:3]
        quad_index = int(parameterCoordinates[p, 0])
        [localCoords, whichCorner, whichPatch] = createLocalParamsExtraordinary(global_quad_params=quadParameters)
        #print "p=%d"%p # todo for p=1 get3x3... fails! -> Resolved(?).
        #print "whichPatch="+str(whichPatch)
        # if there is a specified corner set
        if whichCorner != -1:

            cornerVertexIndex = quad_list[quad_index, whichCorner]

            numberOfEdges = get_num_edges_meeting(AVertexList, cornerVertexIndex)
            #TODO: Check output PROBLEM!
            indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                                   quad_control_point_indices, quad_index, whichCorner)

            coefsRawTemp[0, 0:numberOfEdges, :, :] = ACoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[1, 0:numberOfEdges, :, :] = B1CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[2, 0:numberOfEdges, :, :] = B2CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[3, 0:numberOfEdges, :, :] = CCoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]

            patchCoefsMatrix = getBicubicBezierPointCoefs(localCoords, coefsRawTemp[:, 0:numberOfEdges, :, :])

            coefsMatrix[p][indexMask[:]] = patchCoefsMatrix[:]

        else:
            neighbourMask = get3x3ControlPointIndexMask(quad_list=quad_list,
                                                        quad_control_point_indices=quad_control_point_indices,
                                                        quad_index=quad_index,
                                                        localIndexXY=whichPatch)
            neighbourCoefs = getBezierPointCoefs(localCoords)

            for j in range(3):
                for num_quads in range(3):
                    coefsMatrix[p, neighbourMask[num_quads,j]] = neighbourCoefs[num_quads,j]
    print "Main Loop Coeffs Done."

    return coefsMatrix

# todo || Till here, things seem to be okay. I say "seem to be", as there is no easy way to compare the coefsMatrix
# todo || with the one from MatLab. Compared #elems in both, they are the same. Compared indices of non-zero entries
# todo || , they are the same.

def solve_least_squares_problem(A, b):
    print "A.shape"+str(A.shape) # todo transform to sparse least squares using csr-format for the matrix
    #print A
    print "b.shape "+str(b.shape)
    #print b
    x = 3 * [None]
    for i in range(3): # todo scipy does not support least squares with b.shape = (N,3), but only with (N,1) -> Here one computes the QR three times instead of one time! OPTIMIZE!!!
        b_red = np.array(b[:,i])
        print "\n\n### least squares %d out of 3...\n" % (i+1)
        ret = lin.lsmr(A, b_red, show=True)
        print "done."
        x[i] = ret[0]

    x = scipy.array(x).T
    print "x: shape "+str(x.shape)
    print x
    return x


#####MAIN CODE######
print "### Initialization ###"
print "Reading csv input..."
parameters = np.genfromtxt('Data/Cantilever_try/parameters.csv', delimiter=';')
quads = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_quads_coarse.csv', delimiter=';'), dtype=int)
vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_coarse.csv', delimiter=';'))
fine_vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_fine.csv', delimiter=';'))
print "Done"

print "Reading mat input..."
mat_contents = sio.loadmat('Data/Cantilever_try/cantilever.mat')

A = mat_contents["A"]
B1 = mat_contents["B1"]
B2 = mat_contents["B2"]
C = mat_contents["C"]
regularPoints= mat_contents["regularPoints"]
print "Done."


print "### Preprocessing ###"
# Throw away any datapoints which are NaN or outside the parameter range [0,1]
# since these cause trouble. (+ Scale the resulting ones so that max and min
# param values are 1 and 0 repspectively in both u and v)

write_tensor3_to_csv(A,'A.csv')
write_tensor3_to_csv(B1,'B1.csv')
write_tensor3_to_csv(B2,'B2.csv')
write_tensor3_to_csv(C,'C.csv')

print "Preprocessing of input data..."
[parameters, fine_vertices] = scaleAwayParameters(parameters, fine_vertices)
[newA, newB1, newB2, newC] = sortAB1B2VIndices(A, B1, B2, C)
print "Done."

write_matrix_to_csv(parameters,'parameters.csv')
write_matrix_to_csv(quads,'quads.csv')
write_tensor3_to_csv(newA,'newA.csv')
write_tensor3_to_csv(newB1,'newB1.csv')
write_tensor3_to_csv(newB2,'newB2.csv')
write_tensor3_to_csv(newC,'newC.csv')
write_matrix_to_csv(regularPoints,'regularPoints.csv')

print "### Peters' Scheme ###"
print "fine_vertices.shape = "+str(fine_vertices.shape)
print "Calculating coefs."
coefs = createGlobalControlMeshCoefs(parameters, quads, newA, newB1, newB2, newC, regularPoints)
print "coefs.shape = "+str(coefs.shape)
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
print "joined_verts.shape = "+str(joined_verts.shape)
joined_coefs = sp.vstack([sparse_coefs, fairnessWeight * sparse_fair_coefs])
print "joined_coefs.shape = "+str(joined_coefs.shape)
print "Done."

READ_INPUT_FILE = False

if READ_INPUT_FILE:
    print "Reading input file for skipping infinitely long least squares computation..."
    vertices = read_matrix_from_csv('vertices.csv')
    print "Done."
else:
    print "Least squares..."
    vertices = solve_least_squares_problem(joined_coefs, joined_verts)
    print "Done."
    write_matrix_to_csv(vertices,'vertices.csv')

#plotBezierSurfaceWhole(quads, newA, newB1, newB2, newC, regularPoints, vertices)

#[biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
#csvwrite('biquadraticPatchIndices.csv',biqIndices);
#csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
#csvwrite('bicubicPatchIndices.csv',bicIndices);

#[NURBSMatrix,NURBSIndices] = createNURBSMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('NURBSPatchPoints.csv',NURBSMatrix);
#csvwrite('NURBSPatchIndices.csv',NURBSIndices);
