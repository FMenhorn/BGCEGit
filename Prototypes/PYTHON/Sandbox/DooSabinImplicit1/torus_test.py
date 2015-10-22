from quad import Quad
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from vertex import Vertex
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'anna'
faces = np.array(np.genfromtxt('quads_Torus.csv', delimiter=';'))
verts = np.array(np.genfromtxt('vers_Torus.csv', delimiter=';'))

def getEdgesCentroids(quad):
    v1 = Vertex(0, np.mean([quad.vertices[0], quad.vertices[1]], 0))
    v2 = Vertex(0, np.mean([quad.vertices[1], quad.vertices[2]], 0))
    v3 = Vertex(0, np.mean([quad.vertices[2], quad.vertices[3]], 0))
    v4 = Vertex(0, np.mean([quad.vertices[3], quad.vertices[0]], 0))
    return [v1, v2, v3, v4]

quads = [None]*faces.shape[0]
listOfVertices = []

for i in range(len(verts)):
    listOfVertices.append(Vertex(i, verts[i]))

for i in range(faces.shape[0]):
    face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
    quads[i] = Quad(i, face_vertices)

globalCounter = 0
for quad in quads:
    edges_centroids = getEdgesCentroids(quad)
    C = Vertex(0, quad.computeCentroid)
    q1 = Quad(0, [quad.vertices[0], edges_centroids[0], C, edges_centroids[3]])
    q2 = Quad(0, [edges_centroids[0], quad.vertices[1], edges_centroids[1], C])
    q3 = Quad(0, [edges_centroids[3], C, edges_centroids[2], quad.vertices[3]])
    q4 = Quad(0, [C, edges_centroids[1], quad.vertices[2], edges_centroids[2]])
    Q = [q1, q2, q3, q4]
    for i in range(4):
        edges_centroids_fine = getEdgesCentroids(Q[i])
        C1 = Vertex(0, Q[i].computeCentroid)
        q11 = Quad(0, [Q[i].vertices[0], edges_centroids_fine[0], C, edges_centroids_fine[3]])
        q12 = Quad(0, [edges_centroids_fine[0], Q[i].vertices[1], edges_centroids_fine[1], C])
        q13 = Quad(0, [edges_centroids_fine[3], C, edges_centroids_fine[2], Q[i].vertices[3]])
        q14 = Quad(0, [C, edges_centroids_fine[1], Q[i].vertices[2], edges_centroids_fine[2]])
        even_finer_quads = [q11, q12, q13, q14]
        for j in range(4):
            quad.dooSabinVertices[]

    # edge1_relative_lengths = np.array(quad.vertices[1].coordinates - quad.vertices[0].coordinates)
    #
    # edge2_relative_lengths = np.array(quad.vertices[2].coordinates - quad.vertices[1].coordinates)
    #
    # edge3_relative_lengths = np.array(quad.vertices[3].coordinates - quad.vertices[2].coordinates)
    #
    # edge4_relative_lengths = np.array(quad.vertices[0].coordinates - quad.vertices[3].coordinates)
    #
    # edges_relative_lengths = [edge1_relative_lengths, edge2_relative_lengths, edge3_relative_lengths, edge4_relative_lengths]
    #
    # for j in range(4):
    #     for k in range(4):
    #         coords = quad.vertices[0].coordinates * (j+1)/8*
    #         quad.dooSabinVertices[j*4-1+k] = Vertex(globalCounter, )






