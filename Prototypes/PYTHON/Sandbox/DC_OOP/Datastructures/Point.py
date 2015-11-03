import numpy as np

__author__ = 'benjamin'


class Point(object):
    def __init__(self, coordinates_in):
        if isinstance(coordinates_in, np.ndarray):
            coordinates = coordinates_in.astype(float)
        elif isinstance(coordinates_in, list) or isinstance(coordinates_in, tuple):
            coordinates = np.array(coordinates_in).astype(float)
        else:
            raise Exception('class Point::__init__\n\t' +
                            'Wrong format for coordinates! Given:'+str(type(coordinates_in)) +
                            '\n\tOnly np.ndarray, list and tuple coordinates are accepted! Aborting!')

        self._dimension = coordinates.__len__()
        self._coordinates = coordinates

    def get_position(self):
        return self._coordinates




