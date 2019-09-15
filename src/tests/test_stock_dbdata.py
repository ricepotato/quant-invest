#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

log = logging.getLogger("qi.tests.server.stock_data")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

from common.appctx import AppContext

ctx = {
    "dao":{
        "class":"server.dao.StockDao"
    },
    "rank":{
        "class":"data.rank.Rank"
    },
    "stock_db":{
        "class":"server.data.StockDbData",
        "properties":{
            "dao":{"bean":"dao"},
            "rank":{"bean":"rank"}
        }
    }
}
app_ctx = AppContext(ctx)
class StockDataTestCase(unittest.TestCase):
    def setUp(self):
        self.stock_data = app_ctx.get_bean("stock_db")

    def tearDown(self):
        pass

    def test_stock_data(self):
        params = {"year":"2018", "min_mrkcap":4000}
        res = self.stock_data.get_data("KOSDAQ", **params)
        for item in res:
            log.info(f"{item['company_name']},")

        params = {"year":"2017", "min_mrkcap":1000}
        res = self.stock_data.get_data("KOSPI", **params)
        for item in res:
            log.info(f"{item['company_name']},")

if __name__ == "__main__":
    unittest.main()