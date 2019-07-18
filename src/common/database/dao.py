#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

import logger.logcfg

log = logging.getLogger("qi.common.database.dao")

from database.database import *

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
        #self._projection_query()


    def _query(self):
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

    def _parse_exp(self, key, val):
        try:
            log.debug("_parse_exp key=%s, val=%s", key, val)
            exp = getattr(self.model, key) == val
        except AttributeError as e:
            cf = key.split("_")[-1]
            col_name = key.replace("_{}".format(cf), "")
            log.debug("_parse_exp cf=%s, col_name=%s, val=%s", cf, col_name, val)
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
            if not args[0].rs:
                args[0].rs = list(args[0]._query())
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
        pass

    def one(self):
        pass

    def limit(self, limit):
        pass

    def page(self, limit, offset):
        pass

    def count(self):
        pass

    def order_by(self, order):
        pass

    def projection(self, projection):
        self.projection = projection

    

class UpdateQuery(Query):

    def _update(self, query, **kwargs):
        count = 0
        for item in query:
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
            query = self._get_filter_query(s)
            count = self._update(query, kwargs)
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

    def get_market(self, name):
        with self.db.session_scope() as s:
            obj = s.query(Market).filter(Market.name == name).first()
            if obj:
                res = obj.to_dict()
            else:
                res = None

        return res
                

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

    def insert(self, name, code, category, market):
        obj = self.model(name, code, category, market)
        obj = self._insert(obj)
        return obj.id
    
        



    