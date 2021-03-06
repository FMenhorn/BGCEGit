__author__ = 'benjamin'


def sample_data(f, res, dims):
    if (dims.__len__() / 2) == 2:
        return sample_data2D(f, res, dims)
    elif (dims.__len__() / 2) == 3:
        return sample_data3D(f, res, dims)
    else:
        print "ERROR!"
        quit()


def sample_data3D(f, res, dims):
    import numpy as np
    import itertools as it

    data = {}
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax']+res, res), np.arange(dims['ymin'], dims['ymax']+res, res), np.arange(dims['zmin'], dims['zmax']+res, res)):
        key = (x, y, z)
        x_vec = np.array([x, y, z])
        data[key] = f(x_vec)
    return data


def sample_data2D(f, res, dims):
    import numpy as np
    import itertools as it

    data = {}
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax']+res, res), np.arange(dims['ymin'], dims['ymax']+res, res)):
        key = (x, y)
        x_vec = np.array([x, y])
        data[key] = f(x_vec)
    return data


def sphere_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([4.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([4.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    radius = 2.0
    d = x - center
    return np.dot(d, d) - radius ** 2


def torus_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([4.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([4.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    x=x-center
    R = 2.0
    r = 1.0
    return (np.dot(x,x)+R**2-r**2)**2-4*R**2*(x[0]**2+x[1]**2)


def doubletorus_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([1.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([1.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    x=(x-center)*1.0/2.0
    radius = 4
    return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01
