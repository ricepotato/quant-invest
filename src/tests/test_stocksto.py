#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "data")
comm_path = os.path.join(cur_path, "..", "common")

sys.path.append(base_path)
sys.path.append(comm_path)

from stocksto import StockDbStore
from logger.logcfg import LogCfg
from database.dao import MarketDao, CategoryDao, CompanyDao, FinancialReportDao as FRDao
from database.database import Database

log = logging.getLogger("qi.tests.stocksto")

class TestStockSto(unittest.TestCase):
    def setUp(self):
        log.info("setUp")

        db = Database()
        db.drop_all()
        db.create_all()

        market_dao = MarketDao(db)
        category_dao = CategoryDao(db)
        compay_dao = CompanyDao(db)
        fr_dao = FRDao(db)
        self.store = StockDbStore(market_dao, category_dao, compay_dao, fr_dao)

    def tearDown(self):
        log.info("tearDown")

    def test_sto(self):
        log.info("test_sto")
        id = self.store.add_market("KOSDAQ")
        self.store.add_data(id, [{"num":1, "name":"name1", "code":"001001", 
                                  "category_code":"301001", "desc":u"종목"},
                                  {"num":2, "name":"name2", "code":"001002", 
                                  "category_code":"301001", "desc":u"종목"}])

        res = self.store.get_company_list("KOSDAQ")
        self.assertIsNotNone(res[0])
        self.assertEqual(len(res), 2)

        fr_dict = {"roa":1, "roe":0.3, "per":17.8, "pbr":12, "evebita":33, "market_cap":1000}

        self.store.add_fr(res[0].id, "2018/12", fr_dict)
    
if __name__ == "__main__":
    unittest.main()