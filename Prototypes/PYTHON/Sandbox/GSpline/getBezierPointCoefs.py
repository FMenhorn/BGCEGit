import numpy as np
import math
import scipy.io as sio

def getBezierPointCoefs(localParams):
    '''
    :param localParams: 4-D matrix of some data ;) e.g. (4x4x4x4)
    :return: Spits out a 3x3 matrix of the coefficients on the neighbouring (and central) vertex points to that in the center of the patch, for a point with the local parameters localParams on the patch.
    '''
    coefsMatrix = np.zeros((3,3));
    for i in range(3):
        for j in range(3):
            # -1 since matlab uses indices from 1-3 instead of 0-2 and the
            # bernstein degree is ^2
            print localParams[0]
            controlPointCoef = bernstein(i,2,localParams[0]) * bernstein(j,2,localParams[1]);
            vertexCoefs = getBiquadraticPatchCoefs(i,j);
            coefsMatrix = coefsMatrix + vertexCoefs * controlPointCoef;
    return coefsMatrix;



def getBiquadraticPatchCoefs(i,j):
    '''
    :param i:
    :param j:
    :return:  a matrix with the biquadractic point coefficients of its
    neighbour vertices for the control point (i,j) on the biquadratic patch,
    in the form of a 3x3 matrix of neighbouring vertex point coefs
    '''
    points=np.zeros((3,3));
    # Be careful with matlab/python indexing
    if (i==0):
        if (j==0):
            points[i,j]=1;
        else:
            points[i,j]=0.5;
            points[1,1]=0.5;
    else:
        if (j==2):
            points[i,j]= 0.5;
            points[1,1]= 0.5;
        else:
            points[i,j]=0.25;
            points[i,1]=0.25;
            points[1,j]=0.25;
            points[1,1]=0.25;
    return points;



#### Testing
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


getBezierPointCoefs(np.ones((3,3)))