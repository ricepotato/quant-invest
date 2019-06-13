#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "crawler")
comm_path = os.path.join(cur_path, "..", "common")

sys.path.append(base_path)
sys.path.append(comm_path)

from crawler import Crawler
from common.logger.logger import LogCfg

log = logging.getLogger("qi.tests.crawler")

class TestCrawler(unittest.TestCase):
    def setUp(self):
        log.info("setUp")
        self.crawler = Crawler()

    def tearDown(self):
        log.info("tearDown")

    def test_crawler(self):
        log.info("crawler")
        self.crawler.start()


if __name__ == "__main__":
    unittest.main()