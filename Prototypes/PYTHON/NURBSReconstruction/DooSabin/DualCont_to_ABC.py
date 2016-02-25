__author__ = 'anna'

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from DooSabin import DooSabin
from PetersScheme.Shape import Shape_DooSabin
from vertex_DooSabin  import Vertex_DooSabin


def dooSabin_ABC(verts, faces):

    quads = [None]*faces.shape[0]

    listOfVertices = []
    for i in range(len(verts)):
        listOfVertices.append(Vertex_DooSabin(i, verts[i][0], verts[i][1], verts[i][2]))


    for i in range(faces.shape[0]):
        face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
        quads[i] = Shape_DooSabin(i, face_vertices)

        for vertex in face_vertices:
            vertex.addNeighbouringFace(quads[i])
    #neighbours_test = quads[4].find_neighbors(quads)

    [vertices_refined, faces_refined] = DooSabin(listOfVertices, quads, 0.5, 1)
    [vertices_refined1, faces_refined1] = DooSabin(vertices_refined, faces_refined, 0.5, 2)


    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_aspect('equal')

    for face in faces_refined1:

        n = len(face._vertices)

        x = [face._vertices[i]._coordinates[0] for i in range(n)]
        y = [face._vertices[i]._coordinates[1] for i in range(n)]
        z = [face._vertices[i]._coordinates[2] for i in range(n)]
        vtx = [zip(x,y,z)]
        poly = Poly3DCollection(vtx, alpha = 0.2)
        poly.set_color('b')
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)


    vertA = -1*np.ones((len(verts), 7, 2))
    vertB1 = -1*np.ones((len(verts), 7, 4))
    vertB2 = -1*np.ones((len(verts), 7, 4))
    nonExtraordinaryPoints = -1*np.ones((len(quads), 16))
    vertC = -1*np.ones((len(verts), 7, 2))

    for i in range(len(quads)):
        nonExtraordinaryPoints[i] = [quads[i].ordered_refined_vertices[j]._id for j in range(16)]

    #necessary arrays
    for i in range(len(listOfVertices)):
        for j in range(len(listOfVertices[i].A)):
            vertA[i][j][0] = listOfVertices[i].A[j][1]._id
            vertA[i][j][1] = listOfVertices[i].A[j][1].parentOrigGrid._id
            vertB1[i][j][0] = listOfVertices[i].B1[j][1]._id
            vertB1[i][j][1] = listOfVertices[i].B1[j][1].parentOrigGrid._id
            vertB1[i][j][2] = listOfVertices[i].B1[j][2][0]._id
            vertB1[i][j][3] = listOfVertices[i].B1[j][2][1]._id
            vertB2[i][j][0] = listOfVertices[i].B2[j][1]._id
            vertB2[i][j][1] = listOfVertices[i].B2[j][1].parentOrigGrid._id
            vertB2[i][j][2] = listOfVertices[i].B2[j][2][0]._id
            vertB2[i][j][3] = listOfVertices[i].B2[j][2][1]._id
            vertC[i][j][0] = listOfVertices[i].C[j][1]._id
            vertC[i][j][1] = listOfVertices[i].C[j][1].parentOrigGrid._id

    return vertA, vertB1, vertB2, vertC, nonExtraordinaryPoints