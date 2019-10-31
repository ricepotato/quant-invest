#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

log = logging.getLogger("qi.tests.server.dao")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

from qi.appctx import AppContext
from server.dao import StockDao

class ServerDaoTestCase(unittest.TestCase):
    def setUp(self):
        appctx = AppContext.from_jsonfile("conf/ctx.json")
        factory = appctx.get_bean("factory")
        db = factory.get_db()

    def tearDown(self):
        pass

    def test_dao(self):
        pass

if __name__ == "__main__":
    unittest.main()