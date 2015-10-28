__author__ = 'benjamin'


class Point(object):
    def __init__(self, _position):
        self.dimension = _position.__len__()
        self.coordinates = _position


class Datapoint(Point):
    def __init__(self,_coordinates,_value):
        super(Datapoint, self).__init__(_coordinates)
        self.value = _value

