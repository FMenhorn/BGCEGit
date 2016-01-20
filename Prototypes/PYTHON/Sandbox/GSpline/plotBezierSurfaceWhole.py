import numpy as np
import matplotlib.pyplot as plt
import math

def plotBezierSurfaceWhole(quad_list,
                           AVertexList,
                           B1VertexList,
                           B2VertexList,
                           CVertexList,
                           quad_control_point_indices,
                           control_points):
    """
    Plots the entire Bezier surface
    :param quad_list: List of quads
    :param AVertexList: List of A-Vertices
    :param B1VertexList: List of B1-Vertices
    :param B2VertexList: List of B2-Vertices
    :param CVertexList: List of C-Vertices
    :param quad_control_point_indices: Indices of quad control points
    :param control_points: Control points
    :return: plotHandle: Plot handle
    """

    whichCornerList = [[1, 4], [2, 3]]

    controlVertices = np.zeros((3, 3, 3))

    plotHandle = plt.figure('Name', 'Bezier Surface Plot')
    plt.hold(True)

    for q in range(1, len(quad_list)):
        for j in range(1, 4):
            for i in range(1, 4):
                if ([i, j] == 1) || ([i,j] == 4):
                    whichCorner = whichCornerFun(i, j, whichCornerList)
                    indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList,
                                                           B2VertexList, CVertexList, quad_control_point_indices,
                                                           q, whichCorner)
                    numberOfEdges = len(indexMask[1])
                    As = control_points[indexMask[0][:]][:]
                    B1s = control_points[indexMask[1][:]][:]
                    B2s = control_points[indexMask[2][:]][:]
                    Cs = control_points[indexMask[3][:]][:]
                    Bs = np.concatenate([np.reshape(B1s, [3, 1, numberOfEdges]),
                                         np.reshape(B2s, [3, 1, numberOfEdges])], axis=1)
                    patch = getBicubicPatchIndex(1, As, Bs, Cs)
                    [xx,yy,zz] = bezier(patch, 0.1)
                    plt.surf(xx, yy, zz)
                else:
                    neighbourMask = get3x3ControlPointIndexMask(quad_list, quad_control_point_indices, q, [i,j])
                    for bezierJ in range(0, 2):
                        for bezierI in range(0, 2):
                            controlVertices[:][bezierI][bezierJ] = control_points[neighbourMask[bezierI][bezierJ]][:]

                    APatch = getBiquadraticPatch(controlVertices)
                    [xx, yy, zz] = bezier(APatch, 0.1)
                    plt.surf(xx, yy, zz)

    return plotHandle


def one4toone2(i):
    return (i-1)/3


def whichCornerFun(i, j, whichCornerList):
    return whichCornerList[one4toone2(i)][one4toone2(j)]