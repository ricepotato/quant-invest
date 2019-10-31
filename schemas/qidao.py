#-*- coding: utf-8 -*-

from qi.database.dao import Dao
from .qidb import Market, Category, Company, FinancialReport, ERBoard

class MarketDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = Market

    def insert(self, name):
        obj = Market(name)
        obj = self._insert(obj)
        return obj.id

class CategoryDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = Category        

    def insert(self, code, description):
        obj = self.model(code, description)
        obj = self._insert(obj)
        return obj.id

class CompanyDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = Company

    def insert(self, name, code, category, market, market_cap=None):
        obj = self.model(name, code, category, market_cap, market)
        obj = self._insert(obj)
        return obj.id
    
        
class FinancialReportDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = FinancialReport

    def insert(self, comp_id, period, per, pbr, roa, roe, evebita, marketcap, date_insert=None):
        if date_insert is None:
            date_insert = datetime.datetime.now()
        obj = self.model(comp_id, period, per, pbr, roa, roe, evebita, marketcap, date_insert)
        obj = self._insert(obj)
        return obj.id

class PriceDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = Price

    def insert(self, code, date, open, high, low, close, volume, change):
        obj = self.model(code, date, open, high, low, close, volume, change)
        obj = self._insert(obj)
        return obj.id

    def add_price(self, price_dict):
        count = self.select(code=price_dict["code"], date=price_dict["date"]).count()
        if count <= 0:
            self.insert(price_dict["code"], price_dict["date"], price_dict["open"],
                        price_dict["high"], price_dict["low"], price_dict["close"],
                        price_dict["volume"], price_dict["change"])
        return True
        
class ERBoardDao(Dao):
    def __init__(self, db):
        Dao.__init__(self, db)
        self.model = ERBoard

    def insert(self, code: str, st_date: str, hold: int, period: int, group: int=None) -> int:
        obj = self.model(code, st_date, hold, period, group=group)
        obj = self._insert(obj)
        return obj.id
