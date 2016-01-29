from quadvertGenerator import quad_vert_generator
import scipy.io as sio
import numpy as np
import bernsteinFramework
from helper_functions import *
from createBicubicCoefMatrices import createBicubicCoefMatrices
from createLocalParamsExtraordinary import createLocalParamsExtraordinary
from get3x3ControlPointIndexMask import get3x3ControlPointIndexMask
from getBezierPointCoefs import getBezierPointCoefs
from getBicubicBezierPointCoefs import getBicubicBezierPointCoefs
from getExtraOrdCornerIndexMask import getExtraOrdCornerIndexMask
from sortAB1B2VIndices import sortAB1B2VIndices
from scaleAwayParameters import scaleAwayParameters
from plotBezierSurfaceWhole import plotBezierSurfaceWhole
import csv


vertices, quads, fine_vertices = quad_vert_generator()

# For now we use test data to not run Annas slow code
#dc_to_peter(vertex_list, quad_list)



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

    for i in range(2,7):
        [ACoefsRaw[i, 0:i, :, :],
         B1CoefsRaw[i, 0:i, :, :],
         B2CoefsRaw[i, 0:i, :, :],
         CCoefsRaw[i, 0:i, :, :]] = createBicubicCoefMatrices(i)

     # aroundcorner_indices
    AIndices = np.zeros((1,7))
    B1Indices = np.zeros((1,7))
    B2Indices = np.zeros((1,7))
    CIndices = np.zeros((1,7))

    coefsRawTemp = np.zeros((4,7,4,4))

    for p in range(N):
        #check if on a corner patch : if both coords are outside [0.25,0.75]
        quadParameters = parameterCoordinates[p, 1:3]
        quad_index = int(parameterCoordinates[p, 0])
        [localCoords, whichCorner, whichPatch] = createLocalParamsExtraordinary(global_quad_params=quadParameters)

        # if there is a specified corner set
        if whichCorner != -1:

            cornerVertexIndex = quad_list[quad_index, whichCorner]

            numberOfEdges = getNumOfEdges( AVertexList, cornerVertexIndex)
            #TODO: Check output PROBLEM!
            indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                                   quad_control_point_indices, quad_index, whichCorner)



            coefsRawTemp[0, 0:numberOfEdges, :, :] = ACoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[1, 0:numberOfEdges, :, :] = B1CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[2, 0:numberOfEdges, :, :] = B2CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[3, 0:numberOfEdges, :, :] = CCoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]


            patchCoefsMatrix = getBicubicBezierPointCoefs(localCoords, coefsRawTemp[:, 0:numberOfEdges, :, :])
            print "mask %d", indexMask

            print "p ", p

            print "coefsMatrix[p][indexMask[:]] ", coefsMatrix[p][indexMask[:]]
            print "patchCoefsMatrix[:] ", patchCoefsMatrix[:]

            coefsMatrix[p][indexMask[:]] = patchCoefsMatrix[:]


        else:

            neighbourMask = get3x3ControlPointIndexMask(quad_list=quad_list,
                                                        quad_control_point_indices=quad_control_point_indices,
                                                        quad_index=quad_index,
                                                        localIndexXY=whichPatch)
            neighbourCoefs = getBezierPointCoefs(localCoords)

            for j in range(3):
                for i in range(3):
                    coefsMatrix[p, neighbourMask[i,j]] = neighbourCoefs[i,j]
    return coefsMatrix

#####MAIN CODE######
# Initialization
parameters = np.genfromtxt('Data/Cantilever_try/parameters.csv', delimiter=';')
quads = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_quads_coarse.csv', delimiter=';'), dtype=int)
vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_coarse.csv', delimiter=';'))
fine_vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_fine.csv', delimiter=';'))


mat_contents = sio.loadmat('Data/Cantilever_try/cantilever.mat')

A = mat_contents["A"]#.astype(int)
B1 = mat_contents["B1"]#.astype(int)
B2 = mat_contents["B2"]#.astype(int)
C = mat_contents["C"]##.astype(int)
regularPoints= mat_contents["regularPoints"]#.astype(int)


# Preprocessing
# Throw away any datapoints which are NaN or outside the parameter range [0,1]
# since these cause trouble. (+ Scale the resulting ones so that max and min
# param values are 1 and 0 repspectively in both u and v)

[parameters, fine_vertices] = scaleAwayParameters(parameters, fine_vertices)
[newA, newB1, newB2, newC] = sortAB1B2VIndices(A, B1, B2, C)

print "Loaded data. Creating matrices"
coefs = createGlobalControlMeshCoefs(parameters, quads, newA, newB1, newB2, newC, regularPoints)
print "Done. Matrices created"


## Sparsify ?! Leave out for now

## concatenate matrices with fairness funcional stuff
# joinedCoefs= ...
# joinedVerts= ...
#

print coefs.shape
print fine_vertices.shape
vertices=np.linalg.lstsq(coefs,fine_vertices) # least square here right?
print "small matrix solved, trying big ..."
# otherVertices = np.linalg.lstsq(joinedCoefs,joinedVerts)
print "Plotting doesn't work yet..."
#plotBezierSurfaceWhole(quads, newA, newB1, newB2, newC, regularPoints, vertices)


#[biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
#csvwrite('biquadraticPatchIndices.csv',biqIndices);
#csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
#csvwrite('bicubicPatchIndices.csv',bicIndices);

#[NURBSMatrix,NURBSIndices] = createNURBSMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('NURBSPatchPoints.csv',NURBSMatrix);
#csvwrite('NURBSPatchIndices.csv',NURBSIndices);




