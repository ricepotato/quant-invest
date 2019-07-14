#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

import logger.logcfg

log = logging.getLogger("qi.data.store")

class StockStore(object):
    """ 주식정보를 저장한다. """
    def __init__(self):
        pass

    def add_market(self, market):
        raise NotImplemented

    def add_data(self, market_id, data):
        raise NotImplemented


class StockDbStore(StockStore):
    """ 주식정보를 database 에 저장한다 """
    def __init__(self, mrk_dao, category_dao, company_dao):
        #self.db = db
        self.market = mrk_dao
        self.category = category_dao
        self.company = company_dao

    def add_market(self, market_name):
        market = self.market.get_market(market_name)
        if market is not None:
            id = market.id
        else:
            id = self.market.insert(market_name)
        return id

    def add_data(self, market_id, data):
        for item in data:
            cate_code = item["category_code"]
            desc = item["desc"]
            category_id = self.category.insert(cate_code, desc)
            self.company.insert(item["name"], item["code"], 
                                category_id, market_id)
            
