#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

import common.logger.logcfg
from common.utils.stockreder import SCReader
from common.utils.stocksto import StockDbStore
from common.database import *

log = logging.getLogger("qi.data.csv2sto")

class Csv2Sto(object):
    def __init__(self, reader, sto):
        self.reader = reader
        self.sto = sto

    def c2s(self, market, csv_path):
        data = self.reader.read_file(csv_path)
        market_id = self.sto.add_market(market)
        count = self.sto.add_data(market_id, data)
        return count

def make_stock_sto():
    db = Database()
    mrk_dao = MarketDao(db)
    cate_dao = CategoryDao(db)
    comp_dao = CompanyDao(db)
    sto = StockDbStore(mrk_dao, cate_dao, comp_dao, None)
    return sto

def main():
    cur_path = os.path.dirname(__file__)
    log.info("cur_path=%s", cur_path)

    market_map = {
        "KOSDAQ":"KOSDAQ.csv",
        "KOSPI":"KOSPI.csv"
    }

    reader = SCReader()
    sto = make_stock_sto()
    c2s = Csv2Sto(reader, sto)
    for market, filename in market_map.items():
        data_path = os.path.join(cur_path, "data", filename)
        log.info("market=%s datapath=%s", market, data_path)
        c2s.c2s(market, data_path)

if __name__ == "__main__":
    main()