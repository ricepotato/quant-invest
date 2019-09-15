#-*- coding: utf-8 -*-
import os
import sys
import datetime
import logging

log = logging.getLogger("qi.data.collector")

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error("collector store_data error. company=%s %s", 
                      args[0], e)
            return 0
    return wrapper

class FrCollector(object):
    """ FinancialReport Data 로부터 store 에 data 를 저장한다 """

    def __init__(self, store, fr_data):
        self.store = store
        self.fr_data = fr_data

    def collect(self, market_name):
        log.info("collecting market data. name=%s", market_name)
        res = self.store.get_company_list(market_name)
        
        total = len(res)
        progress = 0
        for company in res:
            cnt = self.store_data(company)
            if cnt > 0:
                log.info("add fr company=%s", str(company.code))
            progress += 1
            log.info("progress (%d/%d)", progress, total)

    @handle_exception
    def store_data(self, company):
        fr_res = self.fr_data.get_data(company.code)
        if not fr_res:
            log.warning("fr_item not exist. comp_code=%s", company.code)
            return None

        cnt = 0
        period_dict = fr_res["period"]
        self.store.update_company(company.id, fr_res["market_cap"])
        for period, fr_item in period_dict.items():
            res = self.store.add_fr(company.id, period, fr_item)
            if res is not None:
                cnt += 1
        return cnt

