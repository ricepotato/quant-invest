#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

from common.database.database import Database
from common.database.dao import *

log = logging.getLogger("qi.tests.database")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        Database().drop_all()
        Database().create_all()

    def tearDown(self):
        pass

    def test_mrk_dao(self):
        market = "KOSDAQ"
        db = Database()
        mrk_dao = MarketDao(db)
        res = mrk_dao.insert(market)
        obj = mrk_dao.get_market(market)
        self.assertEqual(res, obj.id)

        market = "KOSPI"
        res = mrk_dao.insert(market)
        obj = mrk_dao.get_market(market)
        self.assertEqual(res, obj.id)

        market = "NASDAQ"
        obj = mrk_dao.get_market(market)
        self.assertIsNone(obj)

        



if __name__ == "__main__":
    unittest.main()