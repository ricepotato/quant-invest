#-*- coding: utf-8 -*-
import os
import sys
import json
import unittest

try:
    from flask import Flask, jsonify
    from flask_restful import Resource, Api
except ImportError as e:
    log.error("import error. install flask 'pip install flask'")

cur_path = os.path.join(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.join(cur_path, "..", "server"))

sys.path.append(base_path)

from stock import Stock
from server import *
from data import StockData

class FakeStockData(StockData):
    def get_data(self, market, params):
        if market != "KOSDAQ":
            return []
        return [
            {"comp_name":"안랩", "comp_code":"0001", "roa":1, "roe":2, "per":3, "pbr":4, "evebita":5},
            {"comp_name":"카카오", "comp_code":"0002", "roa":1, "roe":2, "per":3, "pbr":4, "evebita":5},
        ]

class TestServer(unittest.TestCase):
    def setUp(self):
        st_data = FakeStockData()
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        api = Api(app)
        rck = {"st_data":st_data}
        api.add_resource(Stock, "/stock", "/stock/<string:market>", 
                         resource_class_kwargs=rck)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_stock(self):
        market = "KOSDAQ"
        res = self.app.get("/stock/{}".format(market))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["market"], market)
        self.assertEqual(len(data["stock"]), 2)

        market = "KOSPI"
        res = self.app.get("/stock/{}".format(market))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["market"], market)
        self.assertEqual(len(data["stock"]), 0)

    def test_get_stock_with_params(self):
        market = "KOSDAQ"
        params = {"min_roa":0.5, "min_per":20, "min_mrkcap":1000, "limit":50}
        res = self.app.get("/stock/{}".format(market), query_string=params)
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":

    unittest.main()



