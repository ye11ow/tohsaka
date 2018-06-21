from abc import ABCMeta, abstractmethod, abstractproperty

class BaseOutputter(metaclass=ABCMeta):

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

