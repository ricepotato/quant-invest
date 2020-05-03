# -*- coding: utf-8 -*-
import unittest

from app.database.mongo import get_db


class MongoTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mongo(self):
        res = get_db()
        assert res
        db = res["qi"]
        rs = db.test.find()
        rs_item = list(rs)
        assert rs_item

