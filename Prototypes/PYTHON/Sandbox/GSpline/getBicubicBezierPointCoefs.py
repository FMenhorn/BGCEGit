import numpy as np
import math
import scipy.io as sio

def getBicubicBezierPointCoefs(localParams, coefs_raw):
    '''

    :param localParams: 4-D matrix of some data ;) e.g. (4x4x4x4)
    :param coefs_raw: 7x7 matrix of some data ;)
    :return: mx4 matrix of the coefficients on the neighbouring (and central) vertex points to that in the center of the patch, for a point with the local parameters localParams on the patch. The first column is the A coef, the second the B1 coefs, the third the B2 coefs, and the fourth the C coefs.
    '''

    m=coefs_raw.shape;
    coefsMatrix = np.zeros((4,m[0],m[1]));
    for j in range (4):
        for i in range (4):
            #bernstein degree is ^3
            controlPointCoef = bernstein(i,3,localParams[0]) * bernstein(j,3,localParams[1]);
            for l in range (m[0]):
                for k in range (4):
                    coefsMatrix[k,l] += coefs_raw[k,l,i,j]* controlPointCoef;
    return coefsMatrix;


### Testing ####


def bincoeff(k, n):
    # calculates binomial coefficient: n!
    # n and k are scalars

    assert n >= k, "n has to be greater or equal to k!"
    assert n >= 0 and k >= 0, "n and k both have to be positive!"

    b = math.factorial(n) / math.factorial(k) / math.factorial(n - k)

    return b

def bernstein(i, n, t):
    # Calculates the i-th bernstein polynomial of degree n at t
    # i, n ,t are numpy arrays
    # Formula: bincoeff(n,i) * t^i * (1-t)^(n-i)

    t_power_i = np.power(t, i)
    t_power_n_i = np.power(np.ones((t.size,)) - t, n - i)
    B = np.multiply(np.multiply(bincoeff(i, n), t_power_i), t_power_n_i)
    return B


mat_contents=sio.loadmat('MatlabTestingData/getBicubicBezierPointCoefs.mat')
oct_a = mat_contents['coefsRawTemp']
getBicubicBezierPointCoefs(np.ones((7,7)),oct_a)