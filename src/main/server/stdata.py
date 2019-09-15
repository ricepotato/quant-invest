
import logging
from abc import ABCMeta, abstractmethod

log = logging.getLogger("qi.server.stdata")

class StockData(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self, market, params):
        pass

class StockDbData(StockData):
    def __init__(self):
        self.dao = None
        self.rank = None
        self._DEFAULT_LIMIT = 50

    def get_data(self, market: str, **kwargs) -> list:
        log.debug("get_data market=%s, kwargs=%s", market, kwargs)
        data = self.dao.get_data(market, **kwargs)
        self.rank.init()
        self.rank.add_rank_column("roa", self.rank.DESC)
        self.rank.add_rank_column("per", self.rank.ASC)
        limit = kwargs.get("limit", self._DEFAULT_LIMIT)
        res = self.rank.get_rank(data)[:limit]
        return res