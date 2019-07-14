#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

cur_path = os.path.dirname(__file__)
comm_path = os.path.abspath(os.path.join(cur_path, "..", "common"))

sys.path.append(comm_path)

import logger.logcfg
from stockreder import SCReader

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

def main():
    pass

if __name__ == "__main__":
    main()