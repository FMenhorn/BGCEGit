# ported from MATLAB/Sandbox/GSpline/getExtraOrdCornerIndexMask.m
import numpy as np

from checkB1B2OrientationReversal import checkB1B2OrientationReversal
from checkB1B2Reversal_opt import checkB1B2Reversal_opt

def getExtraOrdCornerIndexMask(quad_list,AVertexList,B1VertexList,B2VertexList,CVertexList,quad_control_point_indices,quad_index,whichCorner):

    mod_index = lambda i, modul: (i-1)%modul + 1
    shifted_indices = lambda ind, modul: mod_index(np.array(range(modul)) + ind,modul)
    reverse_shifted_indices = lambda ind, modul: mod_index(np.arange(modul,-1,0) + ind,modul)

    cornerVertexIndex = quad_list[quad_index,whichCorner]
    numberOfEdges = getNumOfEdgesMeetingMatlab(AVertexList,cornerVertexIndex) # todo Juan Carlos: with the objects this is very nice.
    quadLocalIndex = np.where(AVertexList[cornerVertexIndex,:,2] == quad_index)
    if checkB1B2Reversal_opt(B1VertexList,quad_list,quad_index,cornerVertexIndex,quad_control_point_indices):
        if checkB1B2OrientationReversal(B2VertexList,B1VertexList,quad_list,quad_index,cornerVertexIndex):
            aroundcorner_indices = reverse_shifted_indices(quadLocalIndex,numberOfEdges)
        else:
            aroundcorner_indices = shifted_indices(quadLocalIndex,numberOfEdges)

        B1Indices = B2VertexList[cornerVertexIndex,aroundcorner_indices,0]
        B2Indices = B1VertexList[cornerVertexIndex,aroundcorner_indices,0]

    else:
        if checkB1B2OrientationReversal(B1VertexList,B2VertexList,quad_list,quad_index,cornerVertexIndex):
            aroundcorner_indices = reverse_shifted_indices(quadLocalIndex,numberOfEdges)
        else:
            aroundcorner_indices = shifted_indices(quadLocalIndex,numberOfEdges)

        B1Indices = B1VertexList[cornerVertexIndex,aroundcorner_indices,0]
        B2Indices = B2VertexList[cornerVertexIndex,aroundcorner_indices,0]

    AIndices = AVertexList[cornerVertexIndex,aroundcorner_indices,0]
    CIndices = CVertexList[cornerVertexIndex,aroundcorner_indices,0]

    indexMask = np.array([[AIndices[:].transpose()],
                          [B1Indices[:].tanspose()],
                          [B2Indices[:].transpose()],
                          [CIndices[:].transpose()]])

    return indexMask