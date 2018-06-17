from abc import ABCMeta, abstractmethod, abstractproperty

class BaseOutputter(metaclass=ABCMeta):

    def __init__(self, config):
        self._config = config
        pass


    @abstractmethod
    def _output(self, item):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractproperty
    def REQUIRED_FIELDS(self):
        pass

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

