
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "main")

sys.path.append(base_path)

from crawler import Crawler

log = logging.getLogger("qi.crawler.crawler")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

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