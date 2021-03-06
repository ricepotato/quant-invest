#-*- coding: utf-8 -*-
import os
import sys
import logging
import unittest

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

from common.logger.logger import LogCfg, qi_logger

log = logging.getLogger("qi.tests.logger")

class TestLogger(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_logger(self):
        self.assertEqual(len(qi_logger.handlers), 1)
        LogCfg()._add_handlers()
        self.assertEqual(len(qi_logger.handlers), 1)
        log.info("test logger")


if __name__ == "__main__":
    unittest.main()