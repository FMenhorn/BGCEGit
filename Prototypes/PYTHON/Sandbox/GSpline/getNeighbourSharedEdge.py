# ported from MATLAB/Sandbox/GSpline/getNeighbourSharedEdge.m

import numpy as np

def getNeighbourSharedEdge(quads,selfIndex,ver1,ver2):

    hasVer1_rowIDX,hasVer1_colIDX = np.where(quads == ver1)
    hasVer2_rowIDX,hasVer2_colIDX = np.where(quads[hasVer1_rowIDX,:] == ver2)

    hasBoth = hasVer1_rowIDX[hasVer2_rowIDX]    # todo this is not understandable...

    quadIndex = hasBoth[hasBoth != selfIndex]

    assert quadIndex is int

    raise Exception("WHAAAAAAAT?!?!?!?")

    return quadIndex