import abc
class ModelDataHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getData(self):
        return NotImplemented
    @abc.abstractmethod
    def getTitle(self):
        return NotImplemented
