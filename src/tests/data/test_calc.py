#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
approot_path = os.path.abspath(os.path.join(cur_path, "..", "..", "main"))
sys.path.append(approot_path)

from data.calc import *
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

    def test_calc_comp(self):

        self.assertEqual(DateCalc("2019-01"), DateCalc("2019-01"))
        self.assertTrue(DateCalc("2019-01") > DateCalc("2018-12"))
        self.assertTrue(DateCalc("2019-03") > DateCalc("2019-02"))
        self.assertTrue(DateCalc("2019-03") < DateCalc("2019-05"))
        self.assertTrue(DateCalc("2018-10") < DateCalc("2019-05"))

    def test_date_calc(self):
        dc = DateCalc("2018-01")
        date_res = dc + 12
        self.assertEqual(str(date_res), "2019-01")
        date_res = dc + 1
        self.assertEqual(str(date_res), "2018-02")
        date_res = dc + 6
        self.assertEqual(str(date_res), "2018-07")
        date_res = dc + 24
        self.assertEqual(str(date_res), "2020-01")
        date_res = dc + 25
        self.assertEqual(str(date_res), "2020-02")

        date_res = dc + 12
        self.assertEqual(str(date_res), "2019-01")

    def test_calc_invalid(self):
        """ 보유기간이 전체기간보다 길다 """
        code = "000660"
        hold = 12
        st_date = "2017-01"
        period = 10
        #with self.assertRaises(DateRangeError) as context:
        res = self.calc.get_result(code, st_date, hold, period)
        self.assertIsNotNone(res["error"])

    def test_calc_invalid_period1(self):
        """ period 값이 크다.현재 날짜보다 크다 """
        code = "000660"
        hold = 6
        period = 10
        st_date = "2019-01"
        res = self.calc.get_result(code, st_date, hold, period)
        self.assertIsNotNone(res["error"])

    def test_calc_invalid_st_date(self):
        code = "000660"
        hold = 6
        period = 10
        st_date = "2199-01"
        res = self.calc.get_result(code, st_date, hold, period)
        self.assertIsNotNone(res["error"])

    def test_calc(self):
        code = "000660"
        hold = 2
        st_date = "2017-01"
        period = 5
        res = self.calc.get_result(code, st_date, hold, period)
        """res_dest = {
            "code":code,
            "avg_er":0,
            "total":{
                "buy":{
                    "price":0,
                    "date":"2017-03-02",
                    "st_date":"2017-03"
                },
                "sell":{
                    "price":0,
                    "date":"2017-06-01",
                    "end_date":"2017-06"
                },
                earning_ratio:0
            },
            "er_list":[
                {"buy":{
                    "price":0,
                    "date":"2017-03-02",
                    "st_date":"2017-03"
                },
                "sell":{
                    "price":0,
                    "date":"2017-06-01",
                    "end_date":"2017-06"
                },
                earning_ratio:0},
                {...},
                {...},
                {...}
            ]
        }"""
        self.assertEqual(res["code"], code)
        self.assertEqual(res["total"]["buy"]["st_date"], st_date)
        self.assertEqual(res["total"]["sell"]["end_date"], "2017-06")

        self.assertEqual(res["er_list"][0]["buy"]["st_date"], st_date)
        self.assertEqual(res["er_list"][0]["sell"]["end_date"], "2017-03")

    def test_calc_get_er(self):
        res = self.calc._get_er(100, 110)
        self.assertEqual(res, 10.0)
        res = self.calc._get_er(100, 90)
        self.assertEqual(res, -10.0)
    
if __name__ == "__main__":
    unittest.main()