#-*- coding: utf-8 -*-
import os
import sys
import unittest
from unittest.mock import Mock, call

from qi.database import DBFactory

class FactoryTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_factory(self):
        db = DBFactory.from_conf("conf/database.ini")
        assert db
        db.drop_all()
        db.create_all()

if __name__ == "__main__":
    unittest.main()