#-*- coding: utf-8 -*-

import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "crawler")

sys.path.append(base_path)

from downloader import CompGuideDownloader

log = logging.getLogger("qi")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
log = logging.getLogger("qi.tests.downloader")

class TestDownloader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_downloader(self):
        comp_ids = ["140860", "182690", "054780"]
        downloader = CompGuideDownloader()
        log.info("download start")
        downloader.start_download(comp_ids)       



if __name__ == "__main__":
    unittest.main()