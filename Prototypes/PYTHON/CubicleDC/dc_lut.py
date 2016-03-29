import numpy as np

'''
def case1(origin, dir1, dir2):
    return np.array([origin + .25 * (dir1 + dir2),
                     origin + .5 * dir1,
                     origin + .5 * dir2]), \
           [[0, 1], [0, 2]]


def case1_rot_pos(origin, dir1, dir2):
    return case1(origin + dir2, dir1, -dir2)


def case1_rot_neg(origin, dir1, dir2):
    return case1(origin + dir1, -dir1, dir2)


def case1_mirr(origin, dir1, dir2):
    return case1(origin + dir1 + dir2, -dir1, -dir2)


def case2(origin, dir1, dir2):
    return (np.array([origin + .5 * (dir1 + dir2),
                      origin + dir2 + .5 * (dir1),
                      origin + .5 * (dir1)]),
            [[0, 1], [0, 2]])


def case2_mirr(origin, dir1, dir2):
    return case2(origin + dir1 + dir2, -dir2, -dir1)


def case2_rot_pos(origin, dir1, dir2):
    return case2(origin + dir2, dir1, -dir2)


def case2_rot_neg(origin, dir1, dir2):
    return case2(origin + dir1, -dir1, dir2)


def case3(origin, dir1, dir2):
    return (np.array([origin + .25 * (dir1 + dir2),
                      origin + .5 * (dir1),
                      origin + .5 * (dir2)]),
            [[0, 1], [0, 2]])


def case3_mirr(origin, dir1, dir2):
    return case3(origin + dir1 + dir2, -dir2, -dir1)


def case3_rot_pos(origin, dir1, dir2):
    return case3(origin + dir2, dir1, -dir2)


def case3_rot_neg(origin, dir1, dir2):
    return case3(origin + dir1, -dir1, dir2)


def case4_1(origin, dir1, dir2):  # connected!
    return (np.array([origin + .75 * (dir1 + dir2),
                      origin + dir1 + .5 * (dir2),
                      origin + dir2 + .5 * (dir1),
                      origin + .25 * (dir1 + dir2),
                      origin + .5 * (dir1),
                      origin + .5 * (dir2)]),
            [[0, 1], [0, 2], [3, 4], [3, 5]])


def case4_1_mirr(origin, dir1, dir2):  # connected!
    return case4_1(origin + dir1, -dir1, dir2)


def case4_2_mirr(origin, dir1, dir2):  # notconnected!
    return case4_1(origin + dir1 + dir2, -dir2, -dir1)


dc_lut = {
    (True, False, False, False): case1,  # 1
    (False, True, False, False): case1_rot_neg,  # 2
    (True, True, False, False): case2_mirr,  # 3
    (False, False, True, False): case1_mirr,  # 4
    (True, False, True, False): case4_1_mirr,  # 5
    (False, True, True, False): case2,  # 6
    (True, True, True, False): case3_rot_pos,  # 7
    (False, False, False, True): case1_rot_pos,  # 8
    (True, False, False, True): case2,  # 9
    (False, True, False, True): case4_1,  # 10
    (True, True, False, True): case3_mirr,  # 11
    (False, False, True, True): case2_mirr,  # 12
    (True, False, True, True): case3_rot_neg,  # 13
    (False, True, True, True): case3,  # 14

}
'''


def case1(origin, dir1, dir2):  # (True, False, False, False)
    return np.array([origin + .25 * (dir1 + dir2),
                     origin + .5 * dir1,
                     origin + .5 * dir2]), \
           [[0, 1], [0, 2]], \
           [4, 0, 3]


def case2(origin, dir1, dir2):  # (False, True, False, False)
    return np.array([origin + .75 * dir1 + .25 * dir2,
                     origin + .5 * dir1,
                     origin + dir1 + .5 * dir2]), \
           [[0, 1], [0, 2]], \
           [4, 0, 1]


def case3(origin, dir1, dir2):  # (True, True, False, False)
    return np.array([origin + .5 * (dir1 + dir2),
                     origin + .5 * dir2,
                     origin + dir1 + .5 * dir2]), \
           [[0, 1], [0, 2]], \
           [4, 3, 1]


def case4(origin, dir1, dir2):  # (False, False, True, False)
    return np.array([origin + .75 * (dir1 + dir2),
                     origin + dir1 + .5 * dir2,
                     origin + .5 * dir1 + dir2]), \
           [[0, 1], [0, 2]], \
           [4, 1, 2]


def case5_1(origin, dir1, dir2):  # (True, False, True, False), connected
    return np.array([origin + .75 * dir1 + .25 * dir2,
                     origin + .5 * dir1,
                     origin + dir1 + .5 * dir2,
                     origin + .25 * dir1 + .75 * dir2,
                     origin + .5 * dir2,
                     origin + dir2 + .5 * dir1]), \
           [[0, 1], [0, 2], [3, 4], [3, 5]], \
           [4, 0, 1, 5, 3, 2]


def case5_2(origin, dir1, dir2):  # (True, False, True, False), unconnected
    return np.array([origin + .25 * (dir1 + dir2),
                     origin + .5 * dir1,
                     origin + .5 * dir2,
                     origin + .75 * (dir1 + dir2),
                     origin + dir1 + .5 * dir2,
                     origin + dir2 + .5 * dir1]), \
           [[0, 1], [0, 2], [3, 4], [3, 5]], \
           [4, 0, 3, 5, 1, 2]


def case6(origin, dir1, dir2):  # (False, True, True, False)
    return np.array([origin + .5 * (dir1 + dir2),
                     origin + .5 * dir1,
                     origin + .5 * dir1 + dir2]), \
           [[0, 1], [0, 2]], \
           [4, 0, 2]


def case7(origin, dir1, dir2):  # (True, True, True, False)
    return np.array([origin + .25 * dir1 + .75 * dir2,
                     origin + .5 * dir2,
                     origin + dir2 + .5 * dir1]), \
           [[0, 1], [0, 2]], \
           [4, 3, 2]


def case8(origin, dir1, dir2):  # (False, False, False, True)
    return case7(origin, dir1, dir2)


def case9(origin, dir1, dir2):  # (True, False, False, True)
    return case6(origin, dir1, dir2)


def case10_1(origin, dir1, dir2):  # (False, True, False, True), connected
    return case5_2(origin, dir1, dir2)


def case10_2(origin, dir1, dir2):  # (False, True, False, True), unconnected
    return case5_1(origin, dir1, dir2)


def case11(origin, dir1, dir2):  # (True, True, False, True)
    return case4(origin, dir1, dir2)


def case12(origin, dir1, dir2):  # (False, False, True, True)
    return case3(origin, dir1, dir2)


def case13(origin, dir1, dir2):  # (True, False, True, True)
    return case2(origin, dir1, dir2)


def case14(origin, dir1, dir2):  # (False, True, True, True)
    return case1(origin, dir1, dir2)


dc_lut = {
    (True, False, False, False): case1,  # 1
    (False, True, False, False): case2,  # 2
    (True, True, False, False): case3,  # 3
    (False, False, True, False): case4,  # 4
    (True, False, True, False): case5_1,  # 5
    (False, True, True, False): case6,  # 6
    (True, True, True, False): case7,  # 7
    (False, False, False, True): case8,  # 8
    (True, False, False, True): case9,  # 9
    (False, True, False, True): case10_1,  # 10
    (True, True, False, True): case11,  # 11
    (False, False, True, True): case12,  # 12
    (True, False, True, True): case13,  # 13
    (False, True, True, True): case14,  # 14
}
