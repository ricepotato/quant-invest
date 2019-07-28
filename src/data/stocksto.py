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
        res = self.market.select(name=market_name).limit(1)
        if res:
            id = res[0].id
        else:
            id = self.market.insert(market_name)
        return id

    def add_category(self, cate_code, desc):
        res = self.category.select(code=cate_code).limit(1)
        if res:
            log.debug("category exist. desc=%s id=%s", desc, str(res[0].id))
            return res[0].id
        else:
            category_id = self.category.insert(cate_code, desc)
            return category_id

    def add_company(self, name, code, category_id, market_id):
        res = self.company.select(code=code).limit(1)
        if res:
            log.debug("company exist. name=%s code=%s", name, code)
        else:
            self.company.insert(name, code, category_id, market_id)
            log.info("add company name=%s code=%s", name, code)

    def add_data(self, market_id, data):
        for item in data:
            cate_code = item["category_code"]
            desc = item["desc"]
            cate_id = self.add_category(cate_code, desc)
            self.add_company(item["name"], item["code"], cate_id, market_id)

    def get_company_list(self, market_name):
        res = self.market.select(name=market_name).first()
        if not res:
            return None
        else:
            return self.company.select(market=res[0].id).all()
            
            
