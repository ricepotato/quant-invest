#-*- coding: utf-8 -*-
import os
import sys
import json
import datetime
import logging

log = logging.getLogger("qi.common.database.dao")

from .database import *

class DatabaseError(Exception):
    pass

class ModelError(DatabaseError):
    pass

class InvalidColumnName(DatabaseError):
    pass

def enum(*seq, **named):
    enums = dict(zip(seq, range(len(seq))), **named)
    rev = dict((val, key) for key, val in enums.items())
    enums["rev_map"] = rev
    return type("Enum", (), enums)

Order = enum(DESC=1, ASC=-1)

op_map = {
    "not":lambda k, v : k != v,
    "lt":lambda k, v : k < v,
    "gt":lambda k, v : k > v,
    "lte":lambda k, v : k <= v,
    "gte":lambda k, v : k >= v,
    "like":lambda k, v : k.like('%{}%'.format(v)),
    "ilike":lambda k, v : k.ilike('%{}%'.format(v)),
    "in":lambda k, v : k.in_(v)
}

order_map = {
    Order.DESC : lambda obj : obj.desc(),
    Order.ASC : lambda obj : obj.asc()
}

class Query(object):
    def __init__(self, db, model, filters):
        self.db = db
        self.model = model
        self.filters = filters
        self.limit_val = None
        self.count_query = False
        self.one_query = None
        self.offset = None
        self.orderby = None

    def _query_for_scalar(self):
        with self.db.session_scope() as s:
            self._get_filter_query(s)
            if self.count_query:
                return self.q.count()
            elif self.one_query:
                return self.q.one().to_dict()
        return None

    def _query_for_list(self):
        with self.db.session_scope() as s:
            self._get_filter_query(s)
            res = map(lambda item : item.to_dict(), self.q)
        return res

    def _get_filter_query(self, session, projection=[]):
        exp_list = []
        for key, val in self.filters.items():
            # attr error
            exp_list.append(self._parse_exp(key, val))

        if projection:
            self.q = self._projection_query(session, projection)
        else:
            self.q = session.query(self.model)

        for exp in exp_list:
            self.q = self.q.filter(exp)

        if self.limit_val is not None:
            self.q = self.q.limit(self.limit_val)
        
        if self.offset is not None:
            self.q = self.q.offset(self.offset)

        if self.orderby is not None:
            for item in self.orderby:
                for column, order in item.items():
                    self.q = self.q.order_by(order_map[order]\
                                             (getattr(self.model, 
                                                      column)))

    def _parse_exp(self, key, val):
        try:
            exp = getattr(self.model, key) == val
        except AttributeError as e:
            cf = key.split("_")[-1]
            col_name = key.replace("_{}".format(cf), "")
            exp = op_map[cf](getattr(self.model, col_name), val)
        return exp

    def _projection_query(self, session, proj):
        column_list = []
        for item in proj:
            try:
                column_list.append(getattr(self.model, item))
            except AttributeError as e:
                raise InvalidColumnName("Invalid Column Name {}".format(item))
        return session.query(*column_list)

class DeleteQuery(Query):
    def delete(self):
        with self.db.session_scope() as s:
            self._get_filter_query(s)
            count = 0
            for item in self.q:
                s.delete(item)
                count += 1
        return count        

class SelectQuery(Query):

    projection = []
    rs = []

    def get_rs(func):
        def warpper(*args, **kwargs):
            if not args[0].rs: # <= self
                args[0].rs = list(args[0]._query_for_list())
            return func(*args, **kwargs)
        return warpper

    @get_rs
    def __len__(self):
        return len(self.rs)

    @get_rs
    def __getitem__(self, item):
        return self.rs[item]

    @get_rs
    def all(self):
        return self.rs
    
    def first(self):
        return self.limit(1)

    def limit(self, limit, offset=0):
        self.limit_val = limit
        self.offset = offset
        return self

    def page(self, page, per_page):
        offset = (page - 1) * per_page
        return {"total":self.count(), "items":self.limit(per_page, offset)}

    def count(self):
        self.count_query = True
        return self._query_for_scalar()

    def order_by(self, order_by=[]):
        self.orderby = order_by
        return self

    def projection(self, projection):
        self.projection = projection

class UpdateQuery(Query):

    def _update(self, **kwargs):
        count = 0
        for item in self.q:
            for key, val in kwargs.items():
                try:
                    setattr(item, key, val)
                except AttributeError as e:
                    msg = "Invalid Columne name {}={}".format(key, val)
                    raise InvalidColumnName(msg)
                count += 1
        return count

    def set(self, **kwargs):
        with self.db.session_scope() as s:
            self._get_filter_query(s)
            count = self._update(**kwargs)
        return count

class Dao(object):
    
    __metaclass__ = Singleton

    def __init__(self, db):
        self.db = db
        self.model = None

    def _insert(self, obj):
        res = None
        with self.db.session_scope() as s:
            s.add(obj)
            s.flush()
            res = obj.to_dict()
        return res

    def select(self, **kwargs):
        return SelectQuery(self.db, self.model, filters=kwargs)

    def update(self, **kwargs):
        return UpdateQuery(self.db, self.model, filters=kwargs)

    def delete(self, **kwargs):
        return DeleteQuery(self.db, self.model, filters=kwargs).delete()


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
        