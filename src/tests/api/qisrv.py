#-*- coding: utf-8 -*-
import os
import sys
import logging
import datetime
import unittest

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, "..", "..", "main"))
sys.path.append(base_path)

from common.api import QIApi

log = logging.getLogger("qi.tests.api.qisrv")

class QIClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api = QIApi()
    
    def tearDown(self):
        pass

    def test(self):
        log.info("qi.client")
        res = self.api.get_stock("KOSDAQ", 2018, min_mrkcap=4000)
        self.assertIsNotNone(res)


if __name__ == "__main__":
    unittest.main()