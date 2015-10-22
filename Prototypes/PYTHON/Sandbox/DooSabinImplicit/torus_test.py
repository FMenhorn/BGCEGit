from quad import Quad
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from DooSabin import DooSabin
from vertex import Vertex
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'anna'
faces = np.array(np.genfromtxt('quads_Torus.csv', delimiter=';'))
verts = np.array(np.genfromtxt('vers_Torus.csv', delimiter=';'))

quads = [None]*faces.shape[0]
listOfVertices = []

for i in range(len(verts)):
    listOfVertices.append(Vertex(i, verts[i]))

for i in range(faces.shape[0]):
    face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
    quads[i] = Quad(i, face_vertices)

for quad in quads:
