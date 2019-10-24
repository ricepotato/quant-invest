#-*- coding: utf-8 -*-
import os
import sys
import logging
import datetime
import httpretty
import unittest

from common.api import QIApi

log = logging.getLogger("qi.tests.api.qisrv")

class QIClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api = QIApi()
    
    def tearDown(self):
        pass

    def test_get_stock(self):
        res = self.api.get_stock("KOSDAQ", 2018, min_mrkcap=4000)
        self.assertIsNotNone(res)

    def test_get_er(self):
        res = self.api.get_er()
        self.assertIsNotNone(res)

    def test_post_delete_er(self):
        res = self.api.post_er("281820", "2017-06", 6, 12)
        self.assertIsNotNone(res)
        res = self.api.delete_er(res["id"])
        self.assertEqual(res["count"], 1)

if __name__ == "__main__":
    unittest.main()