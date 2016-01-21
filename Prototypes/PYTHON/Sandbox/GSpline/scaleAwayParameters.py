import numpy as np
import math
import scipy.io as sio


def scaleAwayParameters(unscaled_params, datapoints):
    '''
    :param unscaled_params:
    :param datapoints:
    :return:
    '''

    quad_ids = np.unique(unscaled_params[:, 0]);
    scaledParams = unscaled_params[
                   (unscaled_params[:, 2] >= 0) * (unscaled_params[:, 1] >= 0) * (unscaled_params[:, 1] <=1) * (
                   unscaled_params[:, 2] <= 1), :]
    throwndata = datapoints[(unscaled_params[:, 2] >= 0)* (unscaled_params[:, 1] >= 0)*(
    unscaled_params[:, 1] <= 1)* (unscaled_params[:, 2] <= 1), :];

    for i in range(len(quad_ids)):
        umax = np.max(scaledParams[(scaledParams[:,0] == quad_ids[i]), 1]);
        umin = np.min(scaledParams[(scaledParams[:,0] == quad_ids[i]), 1]);
        vmax = np.max(scaledParams[(scaledParams[:,0] == quad_ids[i]), 2]);
        vmin = np.min(scaledParams[(scaledParams[:,0] == quad_ids[i]), 2]);

        uscale = umax - umin;
        vscale = vmax - vmin;

        if (uscale):
            scaledParams[(scaledParams[:, 0] == quad_ids[i]), 1] = (scaledParams[(
                scaledParams[:, 0] == quad_ids[i]), 1] - umin) / uscale;

        if (vscale):
            scaledParams[(scaledParams[:, 0] == quad_ids[i]), 2] = (scaledParams[(
                scaledParams[:, 0] == quad_ids[i]), 2] - vmin) / vscale;

    return scaledParams, throwndata;


#####MAIN CODE######
# Initialization
parameters = np.genfromtxt('Data/Cantilever_try/parameters.csv', delimiter=';')
quads = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_quads_coarse.csv', delimiter=';'))
vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_coarse.csv', delimiter=';'))
fine_vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_fine.csv', delimiter=';'))


mat_contents = sio.loadmat('Data/Cantilever_try/cantilever.mat')

A = np.array(mat_contents["A"])
B1 = np.array(mat_contents["B1"])
B2 = np.array(mat_contents["B2"])
C = np.array(mat_contents["C"])

print scaleAwayParameters(parameters, fine_vertices)
