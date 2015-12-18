__author__ = 'benjamin'

import matplotlib.pyplot as plt
import numpy as np

__displacement = [np.array([0.0, 0.0]),
                  np.array([1.0, 0.0]),
                  np.array([1.0, 1.0]),
                  np.array([0.0, 1.0])]

def plot_qt(qt, opt):
    if(qt.is_leaf()):
        __finally_plot_qt(qt, opt)
    else:
        for c in qt.get_children():
            plot_qt(c, opt)


def __finally_plot_qt(qt, opt):
    x = 5*[None]
    y = 5*[None]

    origin = qt.get_origin()
    for i in range(5):
        vtx = origin + __displacement[i%4] * qt.get_size()
        x[i] = vtx[0]
        y[i] = vtx[1]

    plt.plot(x,y,opt)




