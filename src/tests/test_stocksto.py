#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "data")
comm_path = os.path.join(cur_path, "..", "common")

sys.path.append(base_path)
sys.path.append(comm_path)

from stocksto import StockDbStore
from logger.logcfg import LogCfg
from database.dao import MarketDao

log = logging.getLogger("qi.tests.stocksto")

class TestStockSto(unittest.TestCase):
    def setUp(self):
        log.info("setUp")
        market_dao = MarketDao()
        self.store = StockDbStore(market_dao, )

    def tearDown(self):
        log.info("tearDown")

    def test_sto(self):
        log.info("test_sto")
        id = self.store.add_market("KOSDAQ")
        self.store.add_data(id, [{"num":1, "name":"name1", "code":"001001", 
                                  "category_code":"301001"}])

    
if __name__ == "__main__":
    unittest.main()