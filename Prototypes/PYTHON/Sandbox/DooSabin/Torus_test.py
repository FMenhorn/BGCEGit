from quad import Quad
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from DooSabin import DooSabin
from vertex import Vertex
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'anna'

def FaceVerts(face, verts):
    #print(face)
    vtx = []
    for i in range(len(face)):
        print(verts[face[i]])
        vtx.append(verts[face[i]])
    return vtx


faces = np.array(np.genfromtxt('quads_Torus.csv', delimiter=';'))
verts = np.array(np.genfromtxt('vers_Torus.csv', delimiter=';'))

quads = [None]*faces.shape[0]

listOfVertices = []
for i in range(len(verts)):
    listOfVertices.append(Vertex(i, verts[i]))

for i in range(faces.shape[0]):
    face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
    quads[i] = Quad(i, face_vertices, verts)

    for vertex in face_vertices:
        vertex.addNeighbouringFace(quads[i])


#neighbours_test = quads[4].find_neighbors(quads)
[vertices_refined, faces_refined] = DooSabin(listOfVertices, quads, 0.5, verts)
[vertices_refined1, faces_refined1] = DooSabin(vertices_refined, faces_refined, 0.5, verts)

fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')
for face in faces_refined1:
    n = len(face.vertices)
   # print(face.vertices)
    x = [face.vertices[i].coordinates[0] for i in range(n)]
    y = [face.vertices[i].coordinates[1] for i in range(n)]
    z = [face.vertices[i].coordinates[2] for i in range(n)]
    vtx = [zip(x,y,z)]
    poly = Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    ax.add_collection3d(poly)

ax.set_xlim3d(2, 6)
ax.set_ylim3d(2, 6)
ax.set_zlim3d(2, 5)
plt.show()