#-*- coding: utf-8 -*-
import os
import sys
import logging
import datetime
import unittest


cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "data")
comm_path = os.path.join(cur_path, "..", "common")

sys.path.append(base_path)
sys.path.append(comm_path)

from collector import FrCollector

log = logging.getLogger("qi.tests.collector")

class Dictionary(dict):
    
    def __getattr__(self, key):
        return self[key]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class FakeStore(object):

    def __init__(self):
        self.added_fr = []
    
    def get_company_list(self, market_name):
        if market_name != "KOSDAQ":
            return []
        item1 = Dictionary()
        item1.code = "001"
        item1.id = 1

        item2 = Dictionary()
        item2.code = "002"
        item2.id = 2
        return [item1, item2]

    def add_fr(self, comp_id, period, fr_item):
        self.added_fr.append(fr_item)
        return None

class FakeFrData(object):
    
    def get_data(self, comp_code, period):
        data_dict = {
            "001":{
                "2018/12":{"roe":0, "roa":1, "per":2, "pbr":3, "evebtia":4},
                "2017/12":{"roe":0, "roa":1, "per":2, "pbr":3, "evebtia":4},
                "2016/12":{"roe":0, "roa":1, "per":2, "pbr":3, "evebtia":4},
            },
            "002":{
                "2018/12":{"roe":0, "roa":1, "per":2, "pbr":3, "evebtia":4},
                "2017/12":{"roe":0, "roa":1, "per":2, "pbr":3, "evebtia":4},
            }
        }
        try:
            return data_dict[comp_code][period]
        except KeyError as e:
            return None


class TestCollector(unittest.TestCase):
    def setUp(self):
        store = FakeStore()
        fr_data = FakeFrData()

        self.collector = FrCollector(store, fr_data)
    
    def tearDown(self):
        pass

    def test_collector(self):
        pass

    def test_period_list(self):
        self.collector._make_period_list()
        period_list = self.collector.period_list
        now = datetime.datetime.now()
        year = now.year
        cnt = 1
        for period in period_list:
            self.assertTrue(str(year - cnt) in period)
            cnt += 1

    def test_collect(self):
        market_name = "KOSDAQ"
        self.collector.collect(market_name)
        self.assertEqual(len(self.collector.store.added_fr), 5)


if __name__ == "__main__":
    unittest.main()