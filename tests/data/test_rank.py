#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

from data.rank import *

log = logging.getLogger("qi.tests.data.rank")

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def cmp_func(x, y):
    if x is None and y is None:
        return 0
    elif x is None:
        return 1
    elif y is None:
        return -1
    else:
        if x > y:
            return 1
        elif x < y:
            return -1
        else:
            return 0
            
class TestRank(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"name":"st1", "roa":0.5, "per":10.5}, # roa_rank 4 per_rank 5 total_rank 9
            {"name":"st2", "roa":0.5, "per":7.5}, # roa_rank 4 per_rank 3 total_rank 7
            {"name":"st3", "roa":1.5, "per":1.5}, # roa_rank 3 per_rank 1 total_rank 4
            {"name":"st4", "roa":8.5, "per":6.5}, # roa_rank 1 per_rank 2 total_rank 3
            {"name":"st5", "roa":3.5, "per":9.5}, # roa_rank 2 per_rank 4 total_rank 6
        ]
        self.rank = Rank()
        #self.rank.data = data

    def tearDown(self):
        pass

    def test_add(self):
        self.rank.add_rank_column("roa", DESC)
        self.rank.add_rank_column("per", ASC)

        self.assertEqual(self.rank.sort_columns[0]["name"], "roa")
        self.assertEqual(self.rank.sort_columns[0]["order"], DESC)

        self.assertEqual(self.rank.sort_columns[1]["name"], "per")
        self.assertEqual(self.rank.sort_columns[1]["order"], ASC)

    def test_get_rank(self):
        self.rank.add_rank_column("roa", DESC)
        self.rank.add_rank_column("per", ASC)
        res = self.rank.get_rank(self.data)

        self.assertEqual(res[0]["name"], "st4")
        self.assertEqual(res[0]["total_rank"], 3)

        self.assertEqual(res[4]["name"], "st1")
        self.assertEqual(res[4]["total_rank"], 9)

    def test_get_total_rank_prop(self):
        test_data = [
            {"name":"name1", "kor":100, "eng":3.6}, # kor_rank 1 eng_rank 2 total_rank 3
            {"name":"name2", "kor":15, "eng":9.6}, # kor_rank 4 eng_rank 4 total_rank 8
            {"name":"name3", "kor":75, "eng":4.6}, # kor_rank 3 eng_rank 3 total_rank 6
            {"name":"name4", "kor":95, "eng":1.6}, # kor_rank 2 eng_rank 1 total_rank 3
        ]

        self.rank = Rank()
        self.rank.add_rank_column("kor", DESC)
        self.rank.add_rank_column("eng", ASC)
        res = self.rank.get_rank(test_data)
        self.assertEqual(res[0]["total_rank"], 3)
        self.assertEqual(res[3]["total_rank"], 8)

    def test_add_rank_prop(self):
        sored_data = [
            {"name":"name1", "roa":1.6},
            {"name":"name2", "roa":7.6},
            {"name":"name3", "roa":7.6},
            {"name":"name4", "roa":9.6},
        ]
        res_data = self.rank._add_rank_prop(sored_data, "roa")
        self.assertEqual(res_data[0]["roa_rank"], 1)
        self.assertEqual(res_data[1]["roa_rank"], 2)
        self.assertEqual(res_data[2]["roa_rank"], 2)
        self.assertEqual(res_data[3]["roa_rank"], 4)

    def test_rank_none(self):
        sort_list = [1, None, 8, 3, 2, 6, None, 0, 3, 5, 7]
        res = sorted(sort_list, key=cmp_to_key(cmp_func))
        
        self.assertEqual(res[0], 0)
        self.assertEqual(res[1], 1)
        self.assertIsNone(res[-1])

    def test_add_column_invalid_value(self):
        with self.assertRaises(ValueError) as context:
            self.rank.add_rank_column("roe", 5)

    def test_rank_key(self):
        sort_data = [
            {"name":"name1", "roa":1.6},
            {"name":"name2", "roa":7.6},
            {"name":"name3", "roa":7.6},
            {"name":"name3", "roa":None},
            {"name":"name4", "roa":9.6},
        ]

        def roa_comp_func(x, y):
            return cmp_func(x["roa"], y["roa"])

        res = sorted(sort_data, key=cmp_to_key(roa_comp_func))
        self.assertEqual(res[0]["name"], "name1")
        self.assertIsNotNone(res[-1]["name"], "name4")

    def test_rank_include_none(self):
        data = [
            {"name":"st1", "roa":0.5, "per":10.5}, # roa_rank 3 per_rank 4 total_rank 7
            {"name":"st2", "roa":0.5, "per":None}, # roa_rank 3 per_rank 5 total_rank 8
            {"name":"st3", "roa":None, "per":1.5}, # roa_rank 5 per_rank 1 total_rank 6
            {"name":"st4", "roa":8.5, "per":6.5}, # roa_rank 1 per_rank 2 total_rank 3
            {"name":"st5", "roa":3.5, "per":9.5}, # roa_rank 2 per_rank 3 total_rank 5
        ]
        rank = Rank()
        rank.add_rank_column("roa", rank.DESC)
        rank.add_rank_column("per", rank.ASC)

        res_data = rank.get_rank(data)
        self.assertIsNotNone(res_data)
        self.assertEqual(res_data[0]["name"], "st4")
        self.assertEqual(res_data[0]["total_rank"], 3)
        self.assertEqual(res_data[-1]["name"], "st2")
        self.assertEqual(res_data[-1]["total_rank"], 8)

        rank.init()
        rank.add_rank_column("roa", rank.DESC)
        rank.add_rank_column("per", rank.ASC)
        res_data = rank.get_rank(data)
        self.assertIsNotNone(res_data)
        self.assertEqual(res_data[0]["name"], "st4")
        self.assertEqual(res_data[0]["total_rank"], 3)
    
if __name__ == "__main__":
    unittest.main()