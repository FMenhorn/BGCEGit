__author__ = 'erik'
import numpy as np


class Vertex:
    def __init__(self, _id, _x, _y, _z):

        self.id = _id
        self.edges = []
        self.quads = []
        self.coordinates = np.array([_x,_y,_z])

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_quad(self, quad):
        self.quads.append(quad)

    def get_edges(self):
        return self.edges

    def get_quads(self):
        return self.quads

    def get_coordinates(self):
        return self.coordinates
