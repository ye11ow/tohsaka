from abc import ABCMeta, abstractmethod, abstractproperty

class Spell(metaclass=ABCMeta):

    def __init__(self, config):
        self._config = config
        pass

    @property
    @abstractproperty
    def name(self):
        pass

    @property
    @abstractproperty
    def intro(self):
        pass

