"""
Abstract base class for data file reader
"""
# pylint: disable=missing-docstring

from abc import ABCMeta, abstractmethod

class Reader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, data_filename, conf_filename):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def get_valid_keys(self):
        pass

    @abstractmethod
    def set_current_key(self, current_key):
        pass

    @abstractmethod
    def get_current_headers(self):
        pass

    @abstractmethod
    def next(self):
        pass
