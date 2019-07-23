#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "..", "data")

sys.path.append(base_path)

from rank import *

log = logging.getLogger("qi.tests.data.rank")

class TestRank(unittest.TestCase):
    def setUp(self):
        data = [
            {"name":"st1", "roa":0.5, "per":10.5}, # roa_rank 4 per_rank 5 total_rank 9
            {"name":"st2", "roa":0.5, "per":7.5}, # roa_rank 4 per_rank 3 total_rank 7
            {"name":"st3", "roa":1.5, "per":1.5}, # roa_rank 3 per_rank 1 total_rank 4
            {"name":"st4", "roa":8.5, "per":6.5}, # roa_rank 1 per_rank 2 total_rank 3
            {"name":"st5", "roa":3.5, "per":9.5}, # roa_rank 2 per_rank 4 total_rank 6
        ]
        self.rank = Rank(data)

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
        res = self.rank.get_rank()

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

        self.rank = Rank(test_data)
        self.rank.add_rank_column("kor", DESC)
        self.rank.add_rank_column("eng", ASC)
        res = self.rank.get_rank()
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



    
if __name__ == "__main__":
    unittest.main()