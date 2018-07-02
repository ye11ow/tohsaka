from abc import ABCMeta, abstractmethod, abstractproperty
from tohsaka.spells import TohsakaException

class BaseSpell(metaclass=ABCMeta):

    def __init__(self, config):
        if not self._validate_config(config):
            raise TohsakaException('Invalid options. Expected [%s] Actual [%s]' % (', '.join(self.REQUIRED_OPTIONS), ', '.join(config.keys())))

        self.config = config


    def _validate_config(self, options):
        if not isinstance(self.REQUIRED_OPTIONS, list):
            raise TohsakaException('Invalid REQUIRED_OPTIONS. Expected list Actual %s' % (type(self.REQUIRED_OPTIONS)))
        return all(key in options for key in self.REQUIRED_OPTIONS)

    @abstractproperty
    def REQUIRED_OPTIONS(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def intro(self):
        raise NotImplementedError
