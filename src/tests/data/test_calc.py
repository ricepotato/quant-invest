#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
approot_path = os.path.abspath(os.path.join(cur_path, "..", "..", "main"))
sys.path.append(approot_path)

from data.calc import DateCalc
from common.appctx import AppContext

log = logging.getLogger("qi.tests.calc")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.calc")

class CalcTestCase(unittest.TestCase):
    def setUp(self):
        ctx_json = os.path.join(approot_path, "ctx.json")
        appctx = AppContext.from_jsonfile(ctx_json)
        self.calc = appctx.get_bean("calc")

    def tearDown(self):
        pass

    def test_date_calc(self):
        dc = DateCalc("2018-01")
        date_res = dc.add(12)
        self.assertEqual(date_res, "2019-01")
        date_res = dc.add(1)
        self.assertEqual(date_res, "2018-02")
        date_res = dc.add(6)
        self.assertEqual(date_res, "2018-07")
        date_res = dc.add(24)
        self.assertEqual(date_res, "2020-01")
        date_res = dc.add(25)
        self.assertEqual(date_res, "2020-02")

        date_res = dc + 12
        self.assertEqual(str(date_res), "2019-01")

    def test_calc_invalid(self):
        code = "000660"
        hold = 12
        st_date = "2017-01"
        period = 10
        res = self.calc.get_list(code, st_date, hold, period)
        self.assertIsNotNone(res)

    def test_calc_long_period(self):
        code = "000660"
        hold = 12
        st_date = "2017-01"
        period = 48
        with self.assertRaises(TypeError) as context:
            res = self.calc.get_list(code, st_date, hold, period)

    def test_calc(self):
        code = "000660"
        hold = 2
        st_date = "2017-01"
        period = 5
        res = self.calc.get_list(code, st_date, hold, period)
        """res_dest = {
            "code":code,
            "avg_er":0,
            "total":{
                "st":"2017-01", "end":"2017-06", "buy_price":0, "sell_price":0, "earning_ratio":0
            },
            "er_list":[
                {"st":"2017-01", "end":"2017-03", "buy_price":0, "sell_price":0, "earning_ratio":0},
                {"st":"2017-02", "end":"2017-04", "buy_price":0, "sell_price":0, "earning_ratio":0},
                {"st":"2017-03", "end":"2017-05", "buy_price":0, "sell_price":0, "earning_ratio":0},
                {"st":"2017-04", "end":"2017-06", "buy_price":0, "sell_price":0, "earning_ratio":0}
            ]
        }"""
        self.assertEqual(res["code"], code)
        self.assertEqual(res["total"]["st"], st_date)
        self.assertEqual(res["total"]["end"], "2017-06")

        self.assertEqual(res["er_list"][0]["st"], st_date)
        self.assertEqual(res["er_list"][0]["end"], "2017-03")

    def test_calc_get_er(self):
        res = self.calc._get_er(100, 110)
        self.assertEqual(res, 10.0)
        res = self.calc._get_er(100, 90)
        self.assertEqual(res, -10.0)
    
if __name__ == "__main__":
    unittest.main()