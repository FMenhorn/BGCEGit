__author__ = 'anna'
import numpy as np
import matplotlib.pyplot as plt
from quad import Quad
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from DooSabin import DooSabin

def FaceVerts(face, verts):
    vtx = np.array([])
    for i in range(0, 1, len(face)):
        vtx.append(verts[face[i]])
    return vtx


faces = np.array(np.genfromtxt('quads_Torus.csv', delimiter=';'))
verts = np.array(np.genfromtxt('vers_Torus.csv', delimiter=';'))

quads = [None]*faces.shape[0]
for i in range(faces.shape[0]):
    quads[i] = Quad(i, faces.astype(int), verts)

[vertices_refined, faces_refined] = DooSabin(verts, quads, 0.5)
fig = plt.figure()
ax = Axes3D(fig)
ax.set_aspect('equal')

for face in faces_refined:
    print(face)
    x = [vertices_refined[i, 0] for i in face]
    y = [vertices_refined[i, 1] for i in face]
    z = [vertices_refined[i, 2] for i in face]
    vtx = [zip(x,y,z)]
    poly=Poly3DCollection(vtx)
    poly.set_color('b')
    poly.set_edgecolor('k')
    ax.add_collection3d(poly)


ax.set_xlim3d(2, 6)
ax.set_ylim3d(2, 6)
ax.set_zlim3d(2, 5)
plt.show()