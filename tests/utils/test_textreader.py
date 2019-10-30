#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..")

sys.path.append(base_path)

from qi.utils.crawler import CompFileReader

log = logging.getLogger("qi.tests.textreader")

bin_path = os.path.join(cur_path, "bin")

class TextReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.reader = CompFileReader()
        utf8 = os.path.join(bin_path, "text_utf8.html")
        utf16le = os.path.join(bin_path, "text_utf16le.html")
        utf17be = os.path.join(bin_path, "text_utf16be.html")

    def tearDown(self):
        pass

    def test_read(self):
        self.reader.data_path = bin_path
        text = self.reader.read_text("text_utf8")
        self.assertIsNotNone(text)
        text = self.reader.read_text("text_utf16le")
        self.assertIsNotNone(text)
        text = self.reader.read_text("text_utf16be")
        self.assertIsNotNone(text)

        
if __name__ == "__main__":
    unittest.main()
    