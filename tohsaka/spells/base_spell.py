from abc import ABCMeta, abstractmethod, abstractproperty

class BaseSpell(metaclass=ABCMeta):

    def __init__(self, config):
        self._config = config
        pass

    @classmethod
    @abstractmethod
    def name(self):
        pass

    @classmethod
    @abstractmethod
    def intro(self):
        pass

