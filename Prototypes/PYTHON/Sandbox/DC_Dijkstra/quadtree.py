__author__ = 'benjamin'

import numpy as np
from coarsening import coarsen


class Quadtree:

    __displacement = [[np.array([0.0, 0.0]),
                       np.array([1.0, 0.0])],
                      [np.array([0.0, 1.0]),
                       np.array([1.0, 1.0])]]

    def __init__(self, size, origin):
        self.__children = None
        self.__data = set()
        self.__size = size
        self.__origin = origin
        self.__area = {'upper':origin+size*np.array([1,1]), 'lower':origin}
        self.__level = 0
        self.__depth = 0
        self.__parent = None

    def add_dataset(self, dataset):
        for d in dataset:
            #print "adding "+str(d)+" @ "+str(d.get_position())
            data_added = self.add_data(d)
            if not data_added:
                msg = "Adding dataset to quadtree not successful! Data out of range!\n" \
                      "size:\t" + str(self.__size) + "\n" \
                      "origin:\t" + str(self.__origin) + "\n" \
                      "data_position:\t" + str(d.get_position()) + "\n" \
                      "qt depth:\t" + str(self.__depth)
                raise Exception(msg)

    def is_inside(self, data):
        d_pos = data.get_position()
        upper_bound = self.__area['upper']
        lower_bound = self.__area['lower']
        return (all(d_pos <= upper_bound) and all(d_pos >= lower_bound))

    def in_quadrant(self, data):
        middle_pos = self.__origin + np.array([1.0,1.0]) * self.__size * .5
        data_pos = data.get_position()
        j = int(data_pos[0] >= middle_pos[0])
        i = int(data_pos[1] >= middle_pos[1])
        return i, j




    def add_data(self, data):
        if self.is_inside(data): # if data is inside this quadtree, it is added.
            if self.is_leaf():
                if self.is_not_occupied():
                    self.__data.add(data) # store new data here
                    return True # successfully added to this quadtree
                else: # already occupied by data
                    old_data = list(self.__data)
                    self.__data = None
                    self.__init_children()
                    success_old_data = True
                    for d in old_data:
                        success_old_data = success_old_data and self.add_data(d)# store old data in one of the children
                    success_new_data = self.add_data(data) # store new data in one of the children
                    return success_old_data and success_new_data  # successfully added to a new child of the quadtree
            else: # no leaf
                i, j = self.in_quadrant(data) # find out children to which we have to add the data
                success_data = self.__children[i][j].add_data(data) # store data to child
                return success_data
        else:
            return False # data not added.

    def __init_children(self):
        half_size = self.__size/2.0
        self.__children = [[None,None],[None,None]]
        for i in range(2):
            for j in range(2):
                child_origin = self.__origin + self.__displacement[i][j] * half_size
                self.__children[i][j] = Quadtree(half_size, child_origin)
                self.__children[i][j].__add_parent(self)

        self.__increment_depth_to(1)

    def __add_parent(self, parent):
        self.__parent = parent
        self.__level = parent.get_level()+1

    def get_level(self):
        return self.__level

    def get_depth(self):
        return self.__depth

    def __increment_depth_to(self, new_depth):
        if self.__depth < new_depth:
            self.__depth = new_depth
            if not self.is_root():
                self.__parent.__increment_depth_to(self.__depth+1)

    def is_leaf(self):
        return self.__depth == 0

    def is_root(self):
        return self.__level == 0

    def has_only_leaves(self):
        assert not self.is_leaf()
        return all([child.is_leaf() for child in self.get_children()])

    def is_not_occupied(self):
        return self.__data.__len__() == 0

    def is_occupied(self):
        return not self.is_not_occupied()

    def get_children(self):
        return self.__children[0] + self.__children[1]

    def get_data(self):
        if self.is_leaf():
            return self.__data
        else:
            raise Exception("Trying to read data from non leaf node!")

    def get_dataset(self):
        if self.is_leaf():
            if self.is_occupied():
                return self.get_data()
            else:
                raise Exception("Trying to read from empty node!")
        else:
            result_dataset = set()
            for i in range(2):
                for j in range(2):
                    child = self.__children[i][j]
                    if not child.is_leaf() or child.is_occupied():
                        result_dataset.update(child.get_dataset())

            return result_dataset

    def get_origin(self):
        return self.__origin

    def get_size(self):
        return self.__size

    def __coarsen(self, at_depth):
        assert(at_depth > 0)
        if not self.is_leaf() and at_depth > 1:
            self.__depth -= 1
            for c in self.get_children():
                if c.get_depth() is at_depth-1:
                    c.__coarsen(at_depth-1)
        elif not self.is_leaf() and at_depth == 1:
            vertex_set = self.get_dataset()
            coarsened_set = coarsen(vertex_set)
            self.__depth = 0
            self.__children = None
            self.__data = coarsened_set
        else:
            raise Exception("something went wrong...")

    def do_coarsening(self, iterations):
        at_depth = self.get_depth()
        assert(at_depth > 0)
        if iterations == 1:
            self.__coarsen(at_depth)
            return
        elif iterations > 1:
            self.__coarsen(at_depth)
            self.do_coarsening(iterations-1)
            return
        elif iterations == 0:
            return