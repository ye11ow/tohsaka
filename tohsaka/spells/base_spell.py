from abc import ABCMeta, abstractmethod, abstractproperty

class BaseSpell(metaclass=ABCMeta):

    def __init__(self, config, params):
        self.config = config
        self.params = params

        self._replace_params()

    def _replace_params(self):
        for key in self.config:
            value = self.config[key]
            if type(value) == str:
                for param in self.params:
                    value = value.replace('<<%s>>' % param, self.params[param])

                self.config[key] = value

    @classmethod
    @abstractmethod
    def name(self):
        pass

    @classmethod
    @abstractmethod
    def intro(self):
        pass

