#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

from common.appctx import AppContext

log = logging.getLogger("qi.tests.price")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.price")

class PriceDataTestCase(unittest.TestCase):
    def setUp(self):
        ctx_json = os.path.join("conf", "ctx.json")
        appctx = AppContext.from_jsonfile(ctx_json)
        self.price_data = appctx.get_bean("price_data")
        self.price_dao = appctx.get_bean("price_dao")
        self.price_dao.delete()

    def tearDown(self):
        pass

    def test_price(self):
        log.info("test_price")
        res = self.price_data.get_price("004800", "2018-01")
        self.assertEqual(res["date"], "2018-01-02")
        self.assertEqual(res["open"], 81963)

        res = self.price_data.get_price("004800", "2018-01")
        self.assertEqual(res["date"], "2018-01-02")
        self.assertEqual(res["open"], 81963)

        res = self.price_data.get_price("008060", "2017-03")
        self.assertEqual(res["date"], "2017-03-02")
        self.assertEqual(res["close"], 8350)
    
if __name__ == "__main__":
    unittest.main()