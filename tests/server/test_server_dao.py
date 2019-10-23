#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

log = logging.getLogger("qi.tests.server.dao")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

from server.dao import StockDao

class ServerDaoTestCase(unittest.TestCase):
    def setUp(self):
        self.dao = StockDao()

    def tearDown(self):
        pass

    def test_dao(self):
        res = self.dao.get_data("KOSDAQ", year="2018")
        for item in res:
            log.info(item)

if __name__ == "__main__":
    unittest.main()