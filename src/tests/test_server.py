#-*- coding: utf-8 -*-
import os
import sys
import json
import unittest
from unittest.mock import Mock, call

from flask import Flask, jsonify
from flask_restful import Resource, Api

cur_path = os.path.join(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

from server.resources.stock import Stock

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        st_data = Mock()
        st_data.get_data = Mock(return_value=[])
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        api = Api(app)
        rck = {"st_data":st_data}
        api.add_resource(Stock, "/stock/<string:market>/<string:year>", 
                         resource_class_kwargs=rck)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_stock(self):
        market = "KOSDAQ"
        year = "2018"
        res = self.app.get(f"/stock/{market}/{year}")
        res_json = json.loads(res.data)
        self.assertEqual(res_json["market"], market)
        self.assertEqual(res_json["stock_list"], [])

if __name__ == "__main__":
    unittest.main()



