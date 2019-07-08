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

from csv2sto import Csv2Sto
from stocksto import StockStore
from logger.logcfg import LogCfg

log = logging.getLogger("qi.tests.csv2sto")

class FakeReader(object):
    def read_file(self, path):
        return [
            {"num":1, "code":"001002", "name":"name1", 
            "category_code":"801002"},
            {"num":2, "code":"002002", "name":"name3", 
            "category_code":"802002"},
            {"num":3, "code":"003002", "name":"name3", 
            "category_code":"803002"},
        ]

class FakeStore(StockStore):
    def add_market(self, market):
        return 1

    def add_data(self, market_id, data):
        return len(data)

class TestCsv2db(unittest.TestCase):
    def setUp(self):
        log.info("setUp")
        reader = FakeReader()
        db = FakeStore()
        self.c2s = Csv2Sto(reader, db)

    def tearDown(self):
        log.info("tearDown")

    def test_c2d(self):
        log.info("c2s")
        market = "KOSDAQ"
        market_csv = os.path.join(base_path, "{}.csv".format(market))
        res = self.c2s.c2s(market, market_csv)
        self.assertEqual(res, 3)

    
if __name__ == "__main__":
    unittest.main()