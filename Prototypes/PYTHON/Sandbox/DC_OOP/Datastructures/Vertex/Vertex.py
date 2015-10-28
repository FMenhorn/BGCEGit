from Datastructures.BasicDatastructures import Point

__author__ = 'erik'
import numpy as np
from Datastructures import BasicDatastructures


class Vertex3(Point):
    def __init__(self, _id, _x, _y, _z):

        super(Vertex3, self).__init__([_x,_y,_z])
        self.id = _id
        self.edges = []
        self.quads = []

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


class Vertex2(Point):
    def __init__(self, _id, _x, _y):

        super(Vertex2, self).__init__([_x,_y])
        self.id = _id
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edges(self):
        return self.edges

    def get_coordinates(self):
        return self.coordinates
