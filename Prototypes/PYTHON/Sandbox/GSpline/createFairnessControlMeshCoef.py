import numpy as np
from createBicubicCoefMatrices import createBicubicCoefMatrices

def createFairnessControlMeshCoefs(quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                   quad_control_point_indices):
    """
    takes the list of N quads, the corner points and the connectivity
    information and spits out the fairness coefficients as an
    (N*16*3)x(N*16) matrix.
    """
    N = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1] * 3
    M = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1]
    print quad_control_point_indices.shape[1]
    print N
    print M
    coefsMAtrix = np.zeros((N, M))

    """
    precalculate the coefficients between all the vertex control points and
    the bezier control points for 7 different number of intersecting
    edges as a start
    (number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
    first coord, bezier point second coord)
    """

    # extraOrdinaryCoefsRaw = np.zeros((7,4,7,4,4))
    ACoefsRaw = np.zeros((7, 7, 4, 4))
    B1CoefsRaw = np.zeros((7, 7, 4, 4))
    B2CoefsRaw = np.zeros((7, 7, 4, 4))
    CCoefsRaw = np.zeros((7, 7, 4, 4))

    for i in range(2, 7):
        ACoefsRaw[i, 0:i, :, :], B1CoefsRaw[i, 0:i, :, :], B2CoefsRaw[i, 0:i, :, :], CCoefsRaw[i, 0:i, :,
                                                                                     :] = createBicubicCoefMatrices(i)
    for bezierI in range(3):
        for bezierJ in range(3):
            ordinaryCoefsRaw[:, :, bezierI, bezierJ] = getBiquadraticPatchCoefs[bezierI, bezierJ]

    coefsRawTemp = np.zeros((4, 7, 4, 4))

    uu2mat = np.array([[2.0, 2.0, 2.0], [-4.0, -4.0, -4.0], [2.0, 2.0, 2.0]]) / 3
    vv2mat = np.transpose(uu2mat)
    uv2mat = np.array([[1.0, 0.0, -1.0], [0.0, 0.0, 0.0], [-1.0, 0.0, 1.0]])
    uu3mat = np.array(
            [[3.0, 3.0, 3.0, 3.0], [-3.0, -3.0, -3.0, -3.0], [-3.0, -3.0, -3.0, -3.0], [3.0, 3.0, 3.0, 3.0]]) / 3
    vv3mat = np.transpose(uu3mat)
    uv3mat = np.array([[1.0, 0.0, 0.0, -1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [-1.0, 0.0, 0.0, 1.0]])

    biqBezCoefs = np.concatenate((uu2mat, 2 * uv2mat, vv2mat), axis=2);
    bicBezCoefs = np.concatenate((uu3mat, 2 * uv3mat, vv3mat), axis=2);

    whichCornerList = np.array([[1, 4], [2, 3]])

    p = 1
    for q in range(quad_list.shape[0]):
        for j in range(4):
            for i in range(4):
                if i == 1 and j == 1 or i == 4 and j == 4:
                    whichCorner = whichCornerFun(i, j)
                    indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList, B2VertexList,
                                                           CVertexList, quad_control_point_indices, q, whichCorner)
                    numberOfEdges = indexMask.shape[2]

                    coefsRawTemp[0, 0:numberOfEdges, :, :] = ACoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[1, 0:numberOfEdges, :, :] = B1CoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[2, 0:numberOfEdges, :, :] = B2CoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[3, 0:numberOfEdges, :, :] = CCoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]

                    for matType in range(3):
                        bezier_points = np.squeeze(bicBezCoefs[:, :, matType])  # squeeze
                        patchCoefsMAtrix = getPetersControlPointCoefs(bezier_points,
                                                                      coefsRawTemp[:, 0:numberOfEdges - 1, :, :])
                        coefsMatrix[p][indexMask[:]] = patchCoefsMatrix[:]
                        p = p + 1
                else:
                    neighbourMask = get3x3ControlPointIndexMask(quad_list=quad_list,
                                                                quad_control_point_indices=quad_control_point_indices,
                                                                quad_index=q,
                                                                localIndexXY=np.array([i, j]))  # correct??

                    for matType in range(3):
                        bezier_points = np.squeeze(bicBezCoefs[:, :, matType])
                        ordinaryPatchCoefsMAtrix = getPetersControlPointCoefs(bezier_points, coefsRawTemp)
                        coefsMatrix[p][indexMask[:]] = patchCoefsMatrix[:]
                        p = p + 1


def one4toone2(i):
    return (i - 1) / 3


def whichCornerFun(i, j, whichCornerList):
    return whichCornerList[one4toone2(i)][one4toone2(j)]
