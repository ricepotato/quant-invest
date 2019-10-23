#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

from crawler import CompGuideCrawler

log = logging.getLogger("qi")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.crawler")

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = CompGuideCrawler()

    def tearDown(self):
        pass

    def _get_text(self, comp_code):
        bin_path = os.path.join(cur_path, "bin")
        html_filepath = os.path.join(bin_path, f"{comp_code}.html")
        with open(html_filepath, "r") as f:
            text = f.read()
        return text

    def _test_crawler(self):
        comp_code = "053800"
        period = "2018-12"
        
        res = self.crawler.get_fr_data(comp_code, period)
        self.assertEqual(res["comp_code"], comp_code)
        self.assertEqual(res["period"], period)
        #self.assertEqual(res["roa"], 9.75)

    def _test_parse_page(self):
        comp_code = "053800"
        text = self._get_text(comp_code)
        res = self.crawler._parse_page(text)
        self.assertEqual(res["2018-12"]["roa"], "9.75")
        self.assertEqual(res["2017-12"]["per"], "33.03")
        self.assertEqual(res["2016-12"]["roa"], "7.14")

        # includes N/A
        comp_code = "043100"
        text = self._get_text(comp_code)
        res = self.crawler._parse_page(text)
        self.assertEqual(res["2018-12"]["per"], "N/A")

    def test_crawler(self):
        fr_data = self.crawler.get_fr_data("053800")
        log.info(fr_data)

if __name__ == "__main__":
    unittest.main()