#-*- coding: utf-8 -*-
import os
import logging
import unittest

from qi.common import Dictionary
log = logging.getLogger("qi.tests.dictionary")

class DictionaryTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_dictionary(self):
        some_dict = Dictionary()

        some_dict["a"] = "b"
        self.assertEqual(some_dict["a"], "b")
        self.assertEqual(some_dict.a, "b")

if __name__ == "__main__":
    unittest.main()