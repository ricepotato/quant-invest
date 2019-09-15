#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "..", "main")

sys.path.append(base_path)

log = logging.getLogger("qi.tests.server.stdata")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

from common.appctx import AppContext
from server.stdata import StockDbData

ctx = {
    "dao":{
        "class":"server.dao.StockDao"
    },
    "rank":{
        "class":"data.rank.Rank"
    },
    "stock_db":{
        "class":"server.stdata.StockDbData",
        "properties":{
            "dao":{"bean":"dao"},
            "rank":{"bean":"rank"}
        }
    }
}
app_ctx = AppContext(ctx)


class StockDataTestCase(unittest.TestCase):
    def setUp(self):
        self.st_data = app_ctx.get_bean("stock_db")

    def tearDown(self):
        pass

    def test_stdata(self):
        kwargs = {"year":"2018"}
        res = self.st_data.get_data("KOSPI", **kwargs)
        for item in res[:2]:
            log.info(f"{item['company_name']},{item['total_rank']},{item['date_insert']}")

        res = self.st_data.get_data("KOSPI", **kwargs)
        for item in res[:2]:
            log.info(f"{item['company_name']},{item['total_rank']},{item['date_insert']}")

if __name__ == "__main__":
    unittest.main()