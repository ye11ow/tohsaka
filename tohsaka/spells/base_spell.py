from abc import ABCMeta, abstractmethod, abstractproperty

class BaseSpell(metaclass=ABCMeta):

    def __init__(self, config):
        self.config = config

    @classmethod
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def intro(self):
        raise NotImplementedError
