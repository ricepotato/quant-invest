#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

from common.utils.downloader import CompGuideDownloader

log = logging.getLogger("qi")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.downloader")

cur_path = os.path.dirname(__file__)
tmp_path = os.path.join(cur_path, "tmp")

if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

class TestDownloader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_downloader(self):
        comp_ids = ["140860", "182690", "054780"]
        downloader = CompGuideDownloader()
        downloader.path = tmp_path
        log.info("download start")
        downloader.start_download(comp_ids)
        
        paths = map(lambda id: os.path.join(tmp_path, f"{id}.html"), comp_ids)
        for filepath in paths:
            self.assertTrue(os.path.exists(filepath))

if __name__ == "__main__":
    unittest.main()
