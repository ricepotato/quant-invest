#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
approot_path = os.path.abspath(os.path.join(cur_path, "..", "..", "main"))
sys.path.append(approot_path)

from common.appctx import AppContext

log = logging.getLogger("qi")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.erdata")

class CalcTestCase(unittest.TestCase):
    def setUp(self):
        ctx_json = os.path.join(approot_path, "ctx.json")
        appctx = AppContext.from_jsonfile(ctx_json)
        self.er_data = appctx.get_bean("er_data")
        self.er_dao = appctx.get_bean("erboard_dao")
        self.er_dao.delete()

    def tearDown(self):
        pass

    def test_erdata_add(self):
        log.info("test erdata")
        data = {"code":"012630", "st_date":"2017-01", "hold":6, "period":24}
        id = self.er_data.add(data)
        self.assertIsNotNone(id)

    def test_erdata_get(self):
        data = {"code":"012630", "st_date":"2018-10", "hold":6, "period":10}
        id = self.er_data.add(data)
        self.assertIsNotNone(id)
        data = {"code":"029460", "st_date":"2018-10", "hold":6, "period":10}
        id = self.er_data.add(data)
        self.assertIsNotNone(id)

        res = self.er_data.get()
        self.assertIsNotNone(res)
    
if __name__ == "__main__":
    unittest.main()