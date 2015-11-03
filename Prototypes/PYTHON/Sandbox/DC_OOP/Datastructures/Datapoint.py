__author__ = 'benjamin'

import matplotlib.pyplot as plt
from Point import Point


class AbstractDatapoint(Point):
    _id_counter = 0

    def __init__(self, coordinates, value):
        super(AbstractDatapoint, self).__init__(coordinates)
        self._id = self._obtain_id()
        self._value = value

    def get_value(self):
        return self._value

    def get_id(self):
        return self._id

    def _obtain_id(self):
        id = AbstractDatapoint._id_counter
        AbstractDatapoint._id_counter += 1
        return id

class Datapoint2(AbstractDatapoint):
    def __init__(self, coordinates, value):
        super(Datapoint2, self).__init__(coordinates, value)

    def draw(self):
        pos = self.get_position()
        xx = pos[0]
        yy = pos[1]
        if self.get_value() > 0:
            plt.plot(xx,yy,'ro')
        else:
            plt.plot(xx,yy,'bo')


class Datapoint3(AbstractDatapoint):
    # ax where plots are created
    _ax = None

    def __init__(self, coordinates, value):
        super(Datapoint3, self).__init__(coordinates, value)

    def draw(self):
        pos = self.get_position()
        xx = pos[0]
        yy = pos[1]
        zz = pos[2]
        if self.get_value() > 0:
            Datapoint3._ax.scatter(xx,yy,zz,'ro')
        else:
            Datapoint3._ax.scatter(xx,yy,zz,'bo')
