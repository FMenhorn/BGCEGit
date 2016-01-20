# ported from MATLAB/Sandbox/GSpline/getCellsAlongEdge.m

import numpy as np

def getCellsAlongEdge(quad_list, control_point_indices, quad_index, vertex1, vertex2, cellNumbers):

    # quad indices oriented:
    # 4---3
    # |   |
    # 1---2

    assert type(quad_list) is np.ndarray
    assert type(control_point_indices) is np.ndarray
    assert type(quad_index) is int
    assert type(vertex1) is int
    assert type(vertex2) is int
    assert type(cellNumbers) is np.ndarray

    local_control_point_indices = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]).transpose()

    dirOne = np.array([ 1.0, 4.0, 4.0, 1.0])
    dirTwo = np.array([ 1.0, 1.0, 4.0, 4.0])

    neighbourQuad = quad_list[quad_index,:]

    cellIndices = np.zeros(cellNumbers.shape)
    verOneIndex = np.where(neighbourQuad == vertex1)[0]
    verTwoIndex = np.where(neighbourQuad == vertex2)[0]

    verOneLocal = np.array([dirOne(verOneIndex), dirTwo(verOneIndex)])
    verTwoLocal = np.array([dirOne(verTwoIndex), dirTwo(verTwoIndex)])

    directionToGo = (verTwoLocal - verOneLocal)/3.0
    for i in range(len(cellIndices)):
        cellsLocalIndex = verOneLocal + cellNumbers[i]*directionToGo
        local_control_index = local_control_point_indices[cellsLocalIndex[0],cellsLocalIndex[1]]
        cellIndices[i] = control_point_indices[quad_index,local_control_index]

    return cellIndices