import os

from abc import ABCMeta, abstractmethod, abstractproperty

class BaseOutputter(metaclass=ABCMeta):

    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def _output(self):
        raise NotImplementedError

    @abstractmethod
    def _add_item(self, item):
        raise NotImplementedError

    @abstractproperty
    def REQUIRED_FIELDS(self):
        raise NotImplementedError

    def _valid(self, item):
        return all(field in item for field in self.REQUIRED_FIELDS)

    def done(self):
        if not os.path.isdir(self.OUTPUT_FOLDER):
            os.makedirs(self.OUTPUT_FOLDER)

        return self._output()

    def go(self, item):
        if self._valid(item):
            return self._add_item(item)
        else:
            return False
