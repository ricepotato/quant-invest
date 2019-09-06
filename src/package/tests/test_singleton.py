#-*- coding: utf-8 -*-
import os
import logging
import unittest

from qi.patterns import Singleton
log = logging.getLogger("qi.tests.singleton")

class FakeObj(metaclass=Singleton):
    pass

class SingletonTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_singleton(self):
        obj = FakeObj()
        obj.some_prop = 3
        self.assertEqual(FakeObj().some_prop, 3)
        FakeObj().some_prop2 = 25
        self.assertEqual(FakeObj().some_prop2, 25)

if __name__ == "__main__":
    unittest.main()