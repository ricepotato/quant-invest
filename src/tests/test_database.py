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
        #Database().drop_all()
        self.db = Database()
        Database().create_all()
        with self.db.session_scope() as s:
            s.query(Market).delete()

    def tearDown(self):
        pass

    def test_mrk_dao(self):
        db = self.db

        market = "KOSDAQ"
        mrk_dao = MarketDao(db)
        res = mrk_dao.insert(market)

        market = "KOSPI"
        res = mrk_dao.insert(market)

        market = "KOSDAQ"
        rs = mrk_dao.select(name=market)
        self.assertEqual(rs[0].name, market)

        rs = mrk_dao.select(name_like="KO")
        self.assertEqual(len(rs), 2)
        

    def test_dao_limit(self):
        mrk_dao = MarketDao(self.db)
        res = mrk_dao.insert("KOSDAQ")
        res = mrk_dao.insert("KOSPI")
        res = mrk_dao.insert("NASDAQ")

        res = mrk_dao.select().limit(1)
        self.assertEqual(len(res), 1)

        res = mrk_dao.select().limit(2)
        self.assertEqual(len(res), 2)

        res = mrk_dao.select().first()
        self.assertEqual(len(res), 1)


    def test_dao_count(self):
        mrk_dao = MarketDao(self.db)
        res = mrk_dao.insert("KOSDAQ")
        count = mrk_dao.select().count()
        self.assertEqual(count, 1)
        res = mrk_dao.insert("KOSPI")
        res = mrk_dao.select().count()
        self.assertEqual(res, 2)


    def test_dao_page(self):
        mrk_dao = MarketDao(self.db)
        res = mrk_dao.insert("KOSDAQ")
        res = mrk_dao.insert("KOSPI")
        res = mrk_dao.insert("NASDAQ")

        res = mrk_dao.select().page(1, 2)
        self.assertEqual(res["total"], 3)
        self.assertEqual(len(res["items"]), 2)

        res = mrk_dao.select().page(2, 2)
        self.assertEqual(res["total"], 3)
        self.assertEqual(len(res["items"]), 1)

    def test_dao_order(self):
        mrk_dao = MarketDao(self.db)
        res = mrk_dao.insert("A")
        res = mrk_dao.insert("B")
        res = mrk_dao.insert("C")
        res = mrk_dao.insert("D")

        res = mrk_dao.select().order_by([{"name":Order.DESC}])
        self.assertEqual(res[0].name, "D")
        self.assertEqual(res[1].name, "C")

        res = mrk_dao.select().order_by([{"name":Order.ASC}])
        self.assertEqual(res[0].name, "A")
        self.assertEqual(res[1].name, "B")

    def test_dao_update(self):
        mrk_dao = MarketDao(self.db)
        res = mrk_dao.insert("A")
        res = mrk_dao.insert("B")

        res = mrk_dao.update(name="A").set(name="C")
        self.assertEqual(res, 1)

        res = mrk_dao.select(name="C").count()
        self.assertEqual(res, 1)



        



if __name__ == "__main__":
    unittest.main()