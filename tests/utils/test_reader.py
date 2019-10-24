#-*- coding: utf-8 -*-
import os
import sys
import unittest
import logging

from common.utils.stockreder import SCReader

log = logging.getLogger("qi.tests.reader")

def make_test_csv():
    #csv_path = os.path.join(cur_path, "test.csv")
    csv_path = "test.csv"
    with open(csv_path, "w", encoding="UTF8") as f:
        f.write(u"번호,종목코드,기업명,업종코드,업종,상장주식수(주),자본금(원),액면가(원),통화구분,대표전화,주소,총카운트")
        f.write("\r\n")
        f.write(u"9,079160,CJ CGV,105901,\"영화, 비디오물, 방송프로그램 제작 및 배급업\",\"21,161,313\",\"10,580,656,500\",\"500\",원(KRW),02-371-6660,서울특별시 용산구 한강대로23길 55 아이파크몰 6층(한강로동) ,790")

    return csv_path

class SCReaderTestCase(unittest.TestCase):
    def setUp(self):
        log.info("setUp")
        self.reader = SCReader()

    def tearDown(self):
        log.info("tearDown")

    def test_read_kosdaq(self):
        kosdaq_csv = os.path.join("data", "KOSDAQ.csv")
        res = self.reader.read_file(kosdaq_csv)
        self.assertEqual(res[0]["num"], 1)
        log.info("kosdaq len=%d", len(res))

    def test_read_kospi(self):
        kospi_csv = os.path.join("data", "KOSPI.csv")
        res = self.reader.read_file(kospi_csv)
        self.assertEqual(res[0]["num"], 1)
        log.info("kospi len=%d", len(res))

    def test_read_csv(self):
        csv_path = make_test_csv()
        res = self.reader.read_file(csv_path)
        log.info(res)
        self.assertEqual(res[0]["num"], 9)
        self.assertEqual(res[0]["desc"], u"영화, 비디오물, 방송프로그램 제작 및 배급업")

        
if __name__ == "__main__":
    unittest.main()
    