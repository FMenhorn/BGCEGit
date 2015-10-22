__author__ = 'anna'


class Vertex:
    def __init__(self, _id, _coordinates):
        self.id = _id
        self.maltab_id = _id+1
        self.coordinates = _coordinates
        self.neighbouringVertices = []
        self.neighbouringFaces = []
        self.childFace = None
        self.A = []
        self.B1 = []
        self.B2 = []
        self.C = []

    def getId(self):
        return self.id

    def getCoordinates(self):
        return self.coordinates

    def addNeighbouringVertex(self, vertex):
        #vertex should be of the type vertex!
        self.neighbouringVertices.append(vertex)
        return

    def addNeighbouringFace(self, face):
        #Face should be of the type face! Not a list of vertex ids
        self.neighbouringFaces.append(face)
        return


