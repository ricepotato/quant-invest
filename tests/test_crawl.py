# -*- coding: utf-8 -*-
import unittest

from app.data.crawler import CompGuideCrawler


class CrawlTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_crawl(self):
        crawler = CompGuideCrawler()
        data = crawler.get_fr_data("013720")
        assert data
        print(data)
