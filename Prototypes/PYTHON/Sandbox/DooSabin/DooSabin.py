__author__ = 'anna'
import numpy as np
from vertex import Vertex
from quad import Quad

def DooSabin(vertices, faces, alpha, vertsForBenni):
    vertices_refined = []
    faces_refined = []

    vertices_children = [ [] for _ in range(len(vertices))]#[None]*len(vertices)
    edges = []

    #get list of edges
    for face in faces:
        for edge in face.getEdges():
            if not ((edge in edges) or ([edge[1], edge[0]] in edges)):
                edges.append(edge)

    edges_children = [ [] for _ in range(len(edges))]

    for face in faces:
        F = face.centroid
        numberOfVertices = len(face.vertex_ids)

        newVertices = []
        for j in range(numberOfVertices):
            v = Vertex(len(vertices_refined),[face.vertices[j].coordinates[l]*(1 - alpha) + F[l]*alpha for l in range(3)])
            vertices_children[face.vertices[j].id].append([face, v])
            vertices_refined.append(v)

            for edge in face.adjacentEdges(face.vertices[j]):
                if edge in edges:
                    edges_children[edges.index(edge)].append([v, edge.index(face.vertices[j])])
                else:
                    edges_children[edges.index([edge[1], edge[0]])].append([v, 1-edge.index(face.vertices[j])])

            newVertices.append(v)

        new_face = Quad(len(faces_refined), newVertices, vertsForBenni)

        for vertex in newVertices:
            vertex.addNeighbouringFace(new_face)

        faces_refined.append(new_face)

    for vert in vertices:
        n = len(vertices_children[vert.id])
        new_face_vertices = [vertices_children[vert.id][i][1] for i in range(n)]
        parent_faces = [vertices_children[vert.id][i][0] for i in range(n)]
        face_ordered = [vertices_children[vert.id][0][1]]
        current_face = parent_faces[0]
        for i in range(1, n, 1):
            j = 0
            while (not current_face.isAdjacent(parent_faces[j])) or (new_face_vertices[j] in face_ordered):
                j += 1
            face_ordered.append(new_face_vertices[j])
            current_face = parent_faces[j]

        face_object = Quad(len(faces_refined), face_ordered, vertsForBenni)

        for vertex in new_face_vertices:
            vertex.addNeighbouringFace(face_object)

        faces_refined.append(face_object)

    for i in range(len(edges)):
        n = 4 #edge always has four children!
        new_face_vertices_positioning = [edges_children[i][j][1] for j in range(n)]
        new_face_vertices = [edges_children[i][0][0], edges_children[i][1][0]]
        if new_face_vertices_positioning[2] == new_face_vertices_positioning[1]:
            new_face_vertices.append(edges_children[i][2][0])
            new_face_vertices.append(edges_children[i][3][0])
        else:
            new_face_vertices.append(edges_children[i][3][0])
            new_face_vertices.append(edges_children[i][2][0])
        face_object = Quad(len(faces_refined), new_face_vertices, vertsForBenni)

        faces_refined.append(face_object)


    return [vertices_refined, faces_refined]




def addFace(verts):

    return