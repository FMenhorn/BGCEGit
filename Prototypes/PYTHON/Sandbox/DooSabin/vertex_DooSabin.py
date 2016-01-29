__author__ = 'anna'
from Vertex import Vertex

class Vertex_DooSabin(Vertex):
    def __init__(self, id, x, y, z):
     #   self._maltab_id = _id+1
        super(Vertex_DooSabin, self).__init__(id, x, y, z)
        self.neighbouringVertices = []
        self.neighbouringFaces = []
        self.childFace = None
        self.parentOrigGrid = None
        self.A = []
        self.B1 = []
        self.B2 = []
        self.C = []

    def getId(self):
        return self._id

    def getCoordinates(self):
        return self._coordinates

    def addNeighbouringVertex(self, vertex):
        #vertex should be of the type vertex!
        self.neighbouringVertices.append(vertex)
        return

    def addNeighbouringFace(self, face):
        #Face should be of the type face! Not a list of vertex ids
        self.neighbouringFaces.append(face)
        return


