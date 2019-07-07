#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

from common.database.database import *
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

    def test_database(self):
        mrk_dao = MarketDao(engine)
        res = mrk_dao.insert("KOSDAQ")
        self.assertIsNotNone(res)
        mrk_dao.insert("KOSPI")
        self.assertIsNotNone(res)



if __name__ == "__main__":
    unittest.main()