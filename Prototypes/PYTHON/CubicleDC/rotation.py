import numpy as np
from numpy import cos, sin

def rotation_around_pt(rotated_pt, origin, rotation):
    rotated_pt = np.concatenate([rotated_pt,[1]],0)
    a_x = rotation[0]
    a_y = rotation[1]
    a_z = rotation[2]
    c = cos(a_x)
    s = sin(a_x)
    R_x = np.array([[1, 0, 0, 0],
                    [0, c, -s, 0],
                    [0, s, c, 0],
                    [0, 0, 0, 1]])
    c = cos(a_y)
    s = sin(a_y)
    R_y = np.array([[c, 0, s, 0],
                    [0, 1, 0, 0],
                    [-s, 0, c, 0],
                    [0, 0, 0, 1]])
    c = cos(a_z)
    s = sin(a_z)
    R_z = np.array([[c, -s, 0, 0],
                    [s, c, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    t_x = origin[0]
    t_y = origin[1]
    t_z = origin[2]
    T = np.array([[1, 0, 0, -t_x],
                  [0, 1, 0, -t_y],
                  [0, 0, 1, -t_z],
                  [0, 0, 0, 1]])

    T_inv = np.array([[1, 0, 0, t_x],
                      [0, 1, 0, t_y],
                      [0, 0, 1, t_z],
                      [0, 0, 0, 1]])

    return (T_inv.dot(R_z.dot(R_y.dot(R_x.dot(T.dot(rotated_pt))))))[0:3]