#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

from crwaler import CompGuideCrawler

log = logging.getLogger("qi.tests.crawler")

class TestCrawler(unittest.TestCase):
    def setUp(self):
        pass
        self.crawler = CompGuideCrawler()

    def tearDown(self):
        pass

    def test_crawler(self):
        comp_code = "053800"
        
        self.crawler.get_fr_data()


if __name__ == "__main__":
    unittest.main()