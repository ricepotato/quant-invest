#-*- coding: utf-8 -*-
import os
import sys
import json
import unittest

cur_path = os.path.join(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.join(cur_path, "..", "server"))

sys.path.append(base_path)

from server import *

class TestServer(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["msg"], "hello world")

    def test_get_stock(self):
        res = self.app.get("/stock")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["msg"], "stock select")

        market = "KOSDAQ"
        res = self.app.get("/stock/{}".format(market))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["market"], market)

if __name__ == "__main__":
    unittest.main()



