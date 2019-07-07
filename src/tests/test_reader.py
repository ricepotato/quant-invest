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

from stockreder import SCReader
from logger.logcfg import LogCfg

log = logging.getLogger("qi.tests.reader")

class TestReader(unittest.TestCase):
    def setUp(self):
        log.info("setUp")
        self.reader = SCReader()

    def tearDown(self):
        log.info("tearDown")

    def test_read_kosdaq(self):
        kosdaq_csv = os.path.join(base_path, "KOSDAQ.csv")
        res = self.reader.read_file(kosdaq_csv)
        self.assertEqual(res[0]["num"], 1)
        log.info("kosdaq len=%d", len(res))

    def test_read_kospi(self):
        kospi_csv = os.path.join(base_path, "KOSPI.csv")
        res = self.reader.read_file(kospi_csv)
        self.assertEqual(res[0]["num"], 1)
        log.info("kospi len=%d", len(res))
        
if __name__ == "__main__":
    unittest.main()