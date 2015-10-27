_author_ = 'juan carlos'
import stlWrite
import csv
import numpy as np


class MeshManager:
    def __init__(self, _quadlist, _vertlist, _data, _res, _vindex):

        self.verts = _vertlist
        self.quads = _quadlist
        self.data = _data
        self.res = _res
        self.vindex = _vindex
        self.quadslen = self.quads.__len__()  # Initializes at the lenght of list, it can be changed after
        self.vertslen = self.verts.__len__()
        self.vindex_mapping = {}
        self.new_nodes_list = []
        self.new_quads_list = []
        self.delete_quads_list = []

    def generate_edge_usage_dict(self):
        edge_usage_dict = {}  # here we save the quads using a certain edge

        for i in range(self.quadslen):  # traverse all quads
            q = self.quads[i]  # choose one quad

            edge_keys = self.get_quad_edge_list(q)  # keys of the edges

            for e in edge_keys:  # traverse all keys of this quad
                if e in edge_usage_dict:  # if the key is already in global list
                    edge_usage_dict[e].append(i)  # append current quad id, since quad is using this edge
                else:
                    edge_usage_dict[e] = [i]  # add key to list and save quad id, since quad is using this edge

            return edge_usage_dict

    def get_quad_edge_list(self, _quad):
        edges = [(_quad[0], _quad[1]),  # edges of this quad
                 (_quad[1], _quad[2]),
                 (_quad[2], _quad[3]),
                 (_quad[3], _quad[0])]

        edge_keys = []  # keys of the edges
        for e in edges:  # traverse all edges of the quad
            key = tuple(sorted(e))  # calculate corresponding edge key.
            # Keys are made up of the vertex indices belonging to the edge (ascending order!)
            edge_keys.append(key)  # add to key list

        return edge_keys

    def update_mesh(self):
        self.verts += self.new_nodes_list  # append new nodes
        self.quads += self.new_quads_list  # append new quads

        for edge_idx in self.delete_quads_list:  # delete quads not needed anymore
            self.quads[edge_idx] = None
        for i in self.delete_quads_list:
            self.quads[i] = None
        while None in self.quads:
            self.quads.remove(None)

    # searches the corresponding key with a given vertex index
    def search_vertex_key_from_index(self, idx):
        for key in self.vindex:
            if int(self.vindex[key]) == int(idx):
                return key

        print "ERROR! INDEX %d not found" % idx
        quit()

    def add_node(self, _node):
        self.new_nodes_list += _node

    def add_quad(self, _quad):
        self.new_quads_list += _quad

    def delete_quad(self, _quad):
        self.delete_quads_list += _quad

    # exports  to a csv file
    def export_as_csv(self, name):
        with open(name + '_quads.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for d in self.quads:
                csvwriter.writerow(np.array(d))
        with open(name + '_verts.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for d in self.verts:
                csvwriter.writerow(np.array(d))

    # exports a mesh to stl
    def export_as_stl(self, filename):
        faces = []
        for q in self.quads:
            vtx = self.verts[q]
            face = []
            for v in vtx:
                face.append(tuple(v))
            faces.append(face)

        with open(filename, 'wb') as fp:
            writer = stlWrite.ASCII_STL_Writer(fp)
            writer.add_faces(faces)
            writer.close()
