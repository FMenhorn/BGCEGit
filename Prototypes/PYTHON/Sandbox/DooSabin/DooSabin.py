__author__ = 'anna'
import quad
import numpy as np


def DooSabin(vertices, faces, alpha):
    vertices_refined = []
    faces_refined = []

    for i in range(len(faces)):
        F = faces[i].centroid
        numberOfVertices = len(faces[i].vertex_ids)

        for j in range(numberOfVertices):
            vertices_refined.append([vertices[faces[i].vertex_ids[j], l]*(1 - alpha) + F[l]*alpha for l in range(3)])
        faces_refined.append(range(len(vertices_refined)-numberOfVertices, len(vertices_refined), 1))

    return [np.array(vertices_refined), faces_refined]

def addFace(verts):

    return