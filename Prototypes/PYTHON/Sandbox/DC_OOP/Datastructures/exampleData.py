import numpy as np

__author__ = 'benjamin'


def circle_implicit(x,r,o):
    d = o-x
    return np.dot(d,d)-r**2


def doubletorus_implicit(x):
    center = np.array([1.0, 3.0])
    x=(x-center)*1.0/2.0
    return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01


def sphere_implicit(x,r,o):
    d = o-x
    return np.dot(d,d)-r**2

pos1 = (1, 2)
pos2 = (4, 5)
data2 = {pos1: True, pos2: False}

data3 = {(0,0,0): True, (0,0,1): True}

o = np.array([1.0,1.0])
r = .9
res = 1.0/8.0

data_circle = {}

for xx in np.arange(0,2.0+res,res):
    for yy in np.arange(0,2.0+res,res):
        x=np.array([xx,yy])
        data_circle[tuple(x)] = bool(circle_implicit(x,r,o) < 0)

o = np.array([1.0,1.0,1.0])
r = .9
res = 1.0/4.0

data_sphere = {}

for xx in np.arange(0,2.0+res,res):
    for yy in np.arange(0,2.0+res,res):
        for zz in np.arange(0,2.0+res,res):
            x=np.array([xx,yy,zz])
            data_sphere[tuple(x)] = bool(sphere_implicit(x,r,o) < 0)


data_2D_doubletorus = {}

res = 1.0/16.0

for xx in np.arange(0,6.0+res,res):
    for yy in np.arange(0,6.0+res,res):
        x=np.array([xx,yy])
        data_2D_doubletorus[tuple(x)] = bool(doubletorus_implicit(x) < 0)





