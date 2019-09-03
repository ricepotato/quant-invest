#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "crawler")
sys.path.append(base_path)

from transform import Transform

log = logging.getLogger("qi")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
log = logging.getLogger("qi.tests.transform")


class TestStockSto(unittest.TestCase):
    def setUp(self):
        self.trans = Transform()

    def tearDown(self):
        pass

    def test_transform(self):
        self.trans.transform()
    
if __name__ == "__main__":
    unittest.main()