#-*- coding: utf-8 -*-
import os
import sys
import logging
import unittest


cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "data")
comm_path = os.path.join(cur_path, "..", "common")

sys.path.append(base_path)
sys.path.append(comm_path)

from collector import FrCollector
from logger.logcfg import LogCfg

log = logging.getLogger("qi.tests.collector")

class TestCollector(unittest.TestCase):
    def setUp(self):
        self.collector = FrCollector(None, None)
    
    def tearDown(self):
        pass

    def test_collector(self):
        pass

if __name__ == "__main__":
    unittest.main()