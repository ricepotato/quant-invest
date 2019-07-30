

from abc import ABCMeta, abstractmethod

class StockData(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self, market, params):
        pass

class StockDbData(StockData):
    def __init__(self, dao):
        self.dao = dao

    def get_data(self, market, params):
        return []