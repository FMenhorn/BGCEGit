import numpy as np
import matplotlib.pyplot as plt

from Datapoint import Datapoint2, Datapoint3

__author__ = 'benjamin'


class AbstractDataset(object):
    # parses data from a dictionary with {(position): datavalue} and constructs Dataset object out of it.
    # position has to be a tuple!

    _dimension = None

    def __init__(self, resolution):
        self._datapoint_dict = {}
        self._resolution = resolution

    # return number of datapoints in this dataset
    def get_num_datapoints(self):
        return self._datapoint_dict.__len__()

    def get_resolution(self):
        return self._resolution

    # returns a datapoint at position with some checks
    def get_datapoint_at(self, position_or_key):
        key, position = self._transform_to_key_position_pair_w_checks(position_or_key)
        return self._get_datapoint_at(key)

    # same like get_datapoint_at, but without checks
    def _get_datapoint_at(self, key):
        if key in self._datapoint_dict:
            return self._datapoint_dict[key]
        else:
            return None # todo something better to return?

    # adds a new datapoint to the dataset, returns true, if successful
    def add_datapoint(self, position_or_key, value):
        key, position = self._transform_to_key_position_pair_w_checks(position_or_key)
        if self._datapoint_at_exists(key):
            return False
        else:
            self._add_datapoint(key, position, value)
            return True

    # checks for existance of a datapoint in the set
    def datapoint_at_exists(self, position_or_key):
        key, position = self._transform_to_key_position_pair_w_checks(position_or_key)
        return self._datapoint_at_exists(key)

    # same line datapoint_at_exists but without checks
    def _datapoint_at_exists(self, key):
        return key in self._datapoint_dict

    def get_all_dataset_values(self):
        dataset_values = {}
        for key, datapoint in self._datapoint_dict.items():
            dataset_values[key] = datapoint.get_value()

        return dataset_values

    # internal helper function: Transforms a position (tuple or np.ndarray) to a key (tuple) with checks.
    @staticmethod
    def _transform_to_key_position_pair_w_checks(position_or_key):
        if isinstance(position_or_key, tuple) or isinstance(position_or_key, np.ndarray):
            key = tuple(np.array(position_or_key).astype(float))
            position = np.array(position_or_key)
        else: # other dataformats are not supported!
            raise Exception("class Dataset::__transform_to_key_position_pair_w_checks\n\t"
                            "Wrong format for position! Only np.ndarray and tuple supported. Aborting!")
        return key, position

class Dataset2(AbstractDataset):

    _dimension = 2

    def __init__(self, data_dict, resolution):
        super(Dataset2, self).__init__(resolution)
        for key, value in data_dict.items():
            if isinstance(key, tuple):
                position = np.array(key)
                key = tuple(position.astype(float))
                self._datapoint_dict[key] = Datapoint2(position, value)
            else:
                raise Exception('class Dataset::__init__\n\t'
                                'Wrong format for key! Only Tuple keys are accepted! Aborting!')

    # same like add_datapoint, but without checks
    def _add_datapoint(self, key, position, value):
        self._datapoint_dict[key] = Datapoint2(position, value)

    def draw(self):
        for key, datapoint in self._datapoint_dict.items():
            pos = datapoint.get_position()
            xx = pos[0]
            yy = pos[1]
            if datapoint.get_value() > 0:
                plt.plot(xx,yy,'r.')
            else:
                plt.plot(xx,yy,'b.')

class Dataset3(AbstractDataset):
    # ax where plots are created
    _ax = None

    _dimension = 3

    def __init__(self, data_dict, resolution):
        super(Dataset3, self).__init__(resolution)
        for key, value in data_dict.items():
            if isinstance(key, tuple):
                position = np.array(key)
                key = tuple(position.astype(float))
                self._datapoint_dict[key] = Datapoint3(position, value)
            else:
                raise Exception('class Dataset::__init__\n\t'
                                'Wrong format for key! Only Tuple keys are accepted! Aborting!')

    # same like add_datapoint, but without checks
    def _add_datapoint(self, key, position, value):
        self._datapoint_dict[key] = Datapoint3(position, value)

    def draw(self):
        for key, datapoint in self._datapoint_dict.items():
            pos = datapoint.get_position()
            xx = pos[0]
            yy = pos[1]
            zz = pos[2]
            if datapoint.get_value() > 0:
                self._ax.scatter(xx,yy,zz,'r.')
            else:
                self._ax.scatter(xx,yy,zz,'b.')

    def set_ax(self, ax):
        Dataset3._ax = ax
        for key, dp in self._datapoint_dict.items():
            dp.set_ax(ax)