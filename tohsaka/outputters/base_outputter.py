from abc import ABCMeta, abstractmethod, abstractproperty

class BaseOutputter(metaclass=ABCMeta):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def _output(self, item):
        raise NotImplementedError

    @abstractmethod
    def done(self):
        raise NotImplementedError

    @abstractproperty
    def REQUIRED_FIELDS(self):
        raise NotImplementedError

    def _valid(self, item):
        for field in self.REQUIRED_FIELDS:
            if field not in item:
                return False

        return True

    def go(self, item):
        if self._valid(item):
            return self._output(item)
        else :
            return False

