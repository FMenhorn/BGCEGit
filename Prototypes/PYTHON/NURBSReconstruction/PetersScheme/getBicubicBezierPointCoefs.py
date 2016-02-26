import numpy as np
import math
import scipy.io as sio
from bernsteinFramework import *

def getBicubicBezierPointCoefs(localParams, coefs_raw):
    '''

    :param localParams: 4-D matrix of some data ;) e.g. (4x4x4x4)
    :param coefs_raw: 7x7 matrix of some data ;)
    :return: mx4 matrix of the coefficients on the neighbouring (and central) vertex points to that in the center of the patch, for a point with the local parameters localParams on the patch. The first column is the A coef, the second the B1 coefs, the third the B2 coefs, and the fourth the C coefs.
    '''

    m = coefs_raw.shape[1]
    coefsMatrix = np.zeros((4,m))
    for j in range (4):
        for i in range (4):
            #bernstein degree is ^3
            coefsMatrix[:, :] += coefs_raw[:, :, i, j] * bernstein(i, 3, localParams[0]) * bernstein(j, 3, localParams[1])
    return coefsMatrix