import numpy as np
import math

def createBicubicCoefMatrices(num_of_quads):
    """
    Returns a dictionary with the biquadractic point coefficients of its
    neighbour vertices for each control point (i,j) = 1..4 on the bicubic patch,
    in the form of four vectors of neighbouring vertex point coefs

    Input:
        @param num_of_quads number of quads
    """

    # nomenclature following that of paper of Eck, Hoppe (Automatic
    # Reconstruction of B-Spline Surfaces of Arbitrary Topological Type), from
    # which the formulae are also collected. (except that indices of the
    # control points are, following matlab custom, shifted one higher ;-)  -> Not anymore! :P)

    Acoefs = np.zeros((num_of_quads, 4, 4))
    B1coefs = np.zeros((num_of_quads, 4, 4))
    B2coefs = np.zeros((num_of_quads, 4, 4))
    Ccoefs = np.zeros((num_of_quads, 4, 4))

    c = math.cos(2 * math.pi / num_of_quads)
    a = c / (1.0 - c)

    B1coefs[0][0][0] = 0.25
    B2coefs[0][0][0] = 0.25
    Ccoefs[0][0][0] = 0.25
    Acoefs[0][0][0] = 0.25

    B1coefs[0][1][0] = 1.0 / 12
    B2coefs[0][1][0] = 5.0 / 12
    Ccoefs[0][1][0] = 5.0 / 12
    Acoefs[0][1][0] = 1.0 / 12

    B2coefs[1][2][0] = 5.0 / 12
    B1coefs[0][2][0] = 1.0 / 12
    Ccoefs[0][2][0] = 5.0 / 12
    Ccoefs[1][2][0] = 1.0 / 12

    B2coefs[0][3][0] = 0.25
    B1coefs[1][3][0] = 0.25
    Ccoefs[0][3][0] = 0.25
    Ccoefs[1][3][0] = 0.25

    B2coefs[0][1][1] = 5 / 36
    B1coefs[0][1][1] = 5 / 36
    Ccoefs[0][1][1] = (25 + 4 * a) / 36
    Acoefs[0][1][1] = (1 - 4 * a) / 36

    B2coefs[0][2][1] = (5 - 10 * a) / 36
    B1coefs[1][2][1] = (1 + 2 * a) / 36
    Ccoefs[0][2][1] = (25 + 6 * a) / 36
    Ccoefs[1][2][1] = (5 + 2 * a) / 36

    for i in range(0, num_of_quads - 1):
        Ccoefs[i][3][3] = 1 / num_of_quads

    B2coefs[0][3][1] = (1 - 2 * a) / 12
    B1coefs[1][3][1] = (1 - 2 * a) / 12
    Ccoefs[0][3][1] = (5 + 2 * a) / 12
    Ccoefs[1][3][1] = (5 + 2 * a) / 12

    for i in range(0, num_of_quads - 1):
        Ccoefs[i][3][2] += 1 / num_of_quads

    for l in range(0, num_of_quads - 1):
        Ccoefs[l][3][2] += (2 * a / (3 * c * num_of_quads)) * (np.cos(2 * np.pi * (l - 1) / num_of_quads) +
                                                               np.cos(2 * np.pi * (l % num_of_quads) / num_of_quads))
    shiftReversed = shiftReverse(0, num_of_quads)

    for j in range(0, 2):
        for i in range(j, 3):
            i_symm = j
            j_symm = i

            for k in range(0, num_of_quads - 1):
                Acoefs[k][i_symm][j_symm] = Acoefs[shiftReversed[k]][i][j]
                B1coefs[k][i_symm][j_symm] = B2coefs[shiftReversed[k]][i][j]
                B2coefs[k][i_symm][j_symm] = B1coefs[shiftReversed[k]][i][j]
                Ccoefs[k][i_symm][j_symm] = Ccoefs[shiftReversed[k]][i][j]

    if np.mod(num_of_quads, 2) == 1:
        for i in range(1, num_of_quads):
            h_three_coefs_result = h_three_coefs(i, Ccoefs, c, num_of_quads)
            for j in range(0, num_of_quads - 1):
                Ccoefs[k][2][2] -= ((-1) ** i) * h_three_coefs_result[j]
                B1coefs[k][2][2] -= ((-1) ** i) * h_three_coefs_result[j]
                B2coefs[k][2][2] -= ((-1) ** i) * h_three_coefs_result[j]
    else:
        for i in range(1, num_of_quads):
            h_three_coefs_result = h_three_coefs(i, Ccoefs, c, num_of_quads)
            for j in range(0, num_of_quads - 1):
                Ccoefs[k][2][2] -= ((-1) ** i) * (num_of_quads - i) * h_three_coefs_result[j] * 2 / num_of_quads
                B1coefs[k][2][2] -= ((-1) ** i) * (num_of_quads - i) * h_three_coefs_result[j] * 2 / num_of_quads
                B2coefs[k][2][2] -= ((-1) ** i) * (num_of_quads - i) * h_three_coefs_result[j] * 2 / num_of_quads

    # return {'Acoefs': Acoefs, 'B1coefs': B1coefs, 'B2coefs': B2coefs, 'Ccoefs': Ccoefs}
    return Acoefs, B1coefs, B2coefs, Ccoefs


def shiftReverse(ind, modul):
    # Computes a reverse-order index list of length modul-1 starting from index ind
    # Example: shiftReverse(2, 5) returns [2 1 0 4 3]

    shiftReversed = np.mod([ind - i for i in range(0, modul)], modul)
    return shiftReversed


def shifted_indices(ind, modul):
    # Computes a reverse-order index list of length modul-1 starting from index ind
    # Example: shiftReverse(2, 5) returns [2 1 0 4 3]

    shifted = np.mod([ind + i for i in range(0, modul)], modul)
    return shifted


def h_three_coefs(ind, whichArray, c, num_of_quads):
    shiftedIndices = shifted_indices(ind, num_of_quads)
    ans = [0 for i in range(0, len(shiftedIndices))]
    for i in range(0, len(shiftedIndices)):
        ans[i] = (1 - 2 * c / 3) * whichArray[shiftedIndices[i]][3][2] + (2 * c / 3) * whichArray[
            shiftedIndices[i]][3][1]
    return ans
