
import os
import sys
import unittest
import logging

log = logging.getLogger("qi.crawler.crawler")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

class TestCrawler(unittest.TestCase):
    def setUp(self):
        log.info("setUp")

    def tearDown(self):
        log.info("tearDown")

    def test_crawler(self):
        log.info("crawler")


if __name__ == "__main__":
    unittest.main()