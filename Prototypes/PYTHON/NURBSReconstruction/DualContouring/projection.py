import numpy as np


def find_closest_quads(_point, _quadlist, _n_closest):
    d_sq_list = [None] * _quadlist.__len__() # empty list for distances point to all quads
    for i in range(_quadlist.__len__()): # iterate over all quads
        d_sq = _quadlist[i].measure_centroid_distance_squared(_point) # distance to centroid
        d_sq_list[i] = d_sq

    idx_list = sorted(range(len(d_sq_list)), key=lambda k: d_sq_list[k])
    n_closest_idx = idx_list[:_n_closest]

    return n_closest_idx


def create_parameters(verts, quads):
    param = []
    N_closest_candidates = 4 # compute list of N_closest_candidates closest quads

    for vertex in verts['fine']:
        closest_idx_candidates = find_closest_quads(vertex, quads['coarse'], N_closest_candidates) # find N closest quads with fast criterion: distance to centroid

        distance_min = np.inf
        for candidate_idx in closest_idx_candidates: # iterate over all candidates from coarse criterion
            projected_point, distance, u, v = \
                quads['coarse'][candidate_idx].projection_onto_quad(vertex) # find closest quad with fine criterion: projection onto quad

            if abs(distance) < distance_min: # if candidate gives smaller distance, than all candidates before, this is the new reference
                distance_min = abs(distance)
                u_min = u
                v_min = v
                idx_min = candidate_idx

        param.append(np.array([idx_min,u_min,v_min]))

    return np.array(param)