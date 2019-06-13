#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

from common.database.database import *

log = logging.getLogger("qi.tests.database")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_database(self):
        log.info("test database")



if __name__ == "__main__":
    unittest.main()