import numpy as np

__author__ = 'benjamin'


def circle_implicit(x,r,o):
    d = o-x
    return np.dot(d,d)-r**2


def doubletorus_2d_implicit(x):
    center = np.array([1.0, 3.0])
    x=(x-center)*1.0/2.0
    return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01


def doubletorus_3d_implicit(x):
    center = np.array([1.0, 4.0, 4.0])
    x=(x-center)*1.0/2.0
    return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01+x[2]**2


def sphere_implicit(x,r,o):
    d = o-x
    return np.dot(d,d)-r**2

pos1 = (1, 2)
pos2 = (4, 5)
data2 = {pos1: True, pos2: False}

data3 = {(0,0,0): True, (0,0,1): True}

o = np.array([1.0,1.0])
r = .9
res_circle = 1.0/8.0

data_circle = {}

for xx in np.arange(0,2.0+res_circle, res_circle):
    for yy in np.arange(0,2.0+res_circle, res_circle):
        x=np.array([xx,yy])
        data_circle[tuple(x)] = bool(circle_implicit(x,r,o) < 0)

o = np.array([1.0,1.0,1.0])
r = .9
res_sphere = 1.0/4.0

data_sphere = {}

for xx in np.arange(0,2.0+res_sphere,res_sphere):
    for yy in np.arange(0,2.0+res_sphere,res_sphere):
        for zz in np.arange(0,2.0+res_sphere,res_sphere):
            x=np.array([xx,yy,zz])
            data_sphere[tuple(x)] = bool(sphere_implicit(x,r,o) < 0)


data_2D_doubletorus = {}

res_2D_doubletorus = 1.0/8.0

for xx in np.arange(0, 6.0+res_2D_doubletorus, res_2D_doubletorus):
    for yy in np.arange(0, 6.0+res_2D_doubletorus, res_2D_doubletorus):
        x=np.array([xx,yy])
        data_2D_doubletorus[tuple(x)] = bool(doubletorus_2d_implicit(x) < 0)


data_3D_doubletorus = {}

res_3D_doubletorus = 1.0/8.0

for xx in np.arange(0, 8.0+res_3D_doubletorus, res_3D_doubletorus):
    for yy in np.arange(0, 8.0+res_3D_doubletorus, res_3D_doubletorus):
        for zz in np.arange(0, 8.0+res_3D_doubletorus, res_3D_doubletorus):
            x=np.array([xx,yy,zz])
            data_3D_doubletorus[tuple(x)] = bool(doubletorus_3d_implicit(x) < 0)







