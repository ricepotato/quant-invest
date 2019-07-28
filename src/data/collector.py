#-*- coding: utf-8 -*-
import os
import sys
import datetime
import logging

cur_path = os.path.dirname(__file__)
comm_path = os.path.abspath(os.path.join(cur_path, "..", "common"))

sys.path.append(comm_path)

import logger.logcfg

log = logging.getLogger("qi.data.collector")

class FrCollector(object):
    """ FinancialReport Data 로부터 store 에 data 를 저장한다 """

    def __init__(self, store, fr_data):
        self.store = store
        self.fr_data = fr_data
        self.period_list = self._make_period_list()

    def _make_period_list(self):
        now = datetime.datetime.now()
        year = now.year
        self.period_list = map(lambda idx : "{}/12".format(year - idx), range(1, 4))

    def collect(self, market_name):
        res = self.store.get_company_list(market_name)

        for company in res:
            for period in self.period_list:
                fr_item = self.fr_data.get_data(company.code, period)
                if not fr_item:
                    log.warning("fr_item not exist. comp_code=%s, period=%s", 
                                company.code, period)
                    continue
                self.store.add_fr(company.id, period, fr_item)

    
