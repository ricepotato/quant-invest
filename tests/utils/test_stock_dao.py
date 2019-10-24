#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

from common.database.database import Database
from common.database.dao import *
from common.database.stock_dao import *

log = logging.getLogger("qi.tests.stock_dao")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

class TestStockDao(unittest.TestCase):
    def setUp(self):
        #Database().drop_all()
        self.db = Database()
        Database().create_all()
        with self.db.session_scope() as s:
            s.query(Market).delete()
            s.query(Category).delete()
            s.query(FinancialReport).delete()
            s.query(Company).delete()      
        self.dao = StockDao(self.db)  

    def tearDown(self):
        pass

    def test_dao(self):
        mrk_dao = MarketDao(self.db)
        comp_dao = CompanyDao(self.db)
        cate_dao = CategoryDao(self.db)
        fin_dao = FinancialReportDao(self.db)

        # 053800,안랩,105802,소프트웨어 개발 및 공급업

        market = "KOSDAQ"
        mrk_id = mrk_dao.insert(market)
        self.assertIsNotNone(mrk_id)
        cate_id = cate_dao.insert("105802", "소프트웨어 개발 및 공급업")
        self.assertIsNotNone(cate_id)
        comp_id = comp_dao.insert("안랩", "053800", cate_id, mrk_id)
        self.assertIsNotNone(comp_id)
        fin_id = fin_dao.insert(comp_id, "2018/12", 20.34, 2.16, 9.75, 12.08, 18.03, 5538)
        self.assertIsNotNone(fin_id)

        res = self.dao.get_list("KOSDAQ", "2018/12")
        self.assertIsNotNone(res)
        self.assertEqual(res[0]["comp_name"], "안랩")
        self.assertEqual(res[0]["per"], 20.34)

if __name__ == "__main__":
    unittest.main()