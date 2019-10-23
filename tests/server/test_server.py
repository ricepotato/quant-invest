#-*- coding: utf-8 -*-
import os
import sys
import json
import unittest
from unittest.mock import Mock, call

from flask import Flask, jsonify
from flask_restful import Resource, Api

cur_path = os.path.join(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.join(cur_path, "..", "..", "main"))

sys.path.append(base_path)

from server.resources.stock import Stock
from server.resources.er import ERBoard

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        st_data = Mock()
        st_data.get_data = Mock(return_value=[])
        er_data = Mock()
        er_data.get = Mock(return_value=[])
        er_data.add = Mock(return_value=1)
        er_data.delete = Mock(return_value=1)
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        api = Api(app)
        rck = {"st_data":st_data, "er_data":er_data}
        api.add_resource(Stock, "/stock/<string:market>/<string:year>", 
                         resource_class_kwargs=rck)
        api.add_resource(ERBoard, "/er/<int:id>", "/er",
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

    def test_get_er(self):
        res = self.app.get("/er")
        res_json = json.loads(res.data)
        self.assertEqual(res_json, [])

        res = self.app.get("/er/1")
        res_json = json.loads(res.data)
        self.assertEqual(res_json, [])

    def test_post_er(self):
        data = {"code":"000660", "st_date":"2017-01", 
                "hold":6, "period":12}
        res = self.app.post("/er", data=data)
        res_json = json.loads(res.data)
        self.assertEqual(res_json["id"], 1)

    def test_delete_er(self):
        res = self.app.delete("/er/1")
        res_json = json.loads(res.data)
        self.assertEqual(res_json["count"], 1)

if __name__ == "__main__":
    unittest.main()



