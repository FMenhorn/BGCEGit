import numpy as np
from BasicDatastructures import Datapoint

__author__ = 'benjamin'


class Dataset(object):
    # parses data from a dictionary with {(position): datavalue} and constructs Dataset object out of it.
    # position has to be a tuple!
    def __init__(self, data_dict):
        self._datapoint_dict = {}
        for key, value in data_dict.items():
            if isinstance(key, tuple):
                position = np.array(key)
                self._datapoint_dict[key] = Datapoint(position, value)
            else:
                raise Exception('class Dataset::__init__\n\t'
                                'Wrong format for key! Only Tuple keys are accepted! Aborting!')

    # return number of datapoints in this dataset
    def get_num_datapoints(self):
        return self._datapoint_dict.__len__()

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

    # same like add_datapoint, but without checks
    def _add_datapoint(self, key, position, value):
        self._datapoint_dict[key] = Datapoint(position, value)

    # checks for existance of a datapoint in the set
    def datapoint_at_exists(self, position_or_key):
        key, position = self._transform_to_key_position_pair_w_checks(position_or_key)
        return self._datapoint_at_exists(key)

    # same line datapoint_at_exists but without checks
    def _datapoint_at_exists(self, key):
        return key in self._datapoint_dict

    # internal helper function: Transforms a position (tuple or np.ndarray) to a key (tuple) with checks.
    @staticmethod
    def _transform_to_key_position_pair_w_checks(position_or_key):
        if isinstance(position_or_key, tuple):
            key = position_or_key
            position = np.array(key)
        elif isinstance(position_or_key, np.ndarray): # converting position into tuple from np.ndarray
            key = tuple(position_or_key)
            position = position_or_key
        else: # other dataformats are not supported!
            raise Exception("class Dataset::__transform_to_key_position_pair_w_checks\n\t"
                            "Wrong format for position! Only np.ndarray and tuple supported. Aborting!")
        return key, position
