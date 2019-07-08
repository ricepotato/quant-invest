#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

import logger.logcfg

log = logging.getLogger("qi.common.database.dao")

from sqlalchemy.orm import sessionmaker
from database.database import *

class Dao(object):
    def __init__(self, engine=None):
        self.db = Database()

    def _insert(self, obj):
        with self.db.session_scope() as s:
            s.add(obj)
            s.flush()
            res = obj.to_dict()
        return res

class MarketDao(Dao):
    def insert(self, name):
        obj = Market(name)
        obj = self._insert(obj)
        return obj.id

class CategoryDao(Dao):
    def insert(self, code, description):
        obj = Category(code, description)
        obj = self._insert(obj)
        return obj.id

class CompanyDao(Dao):
    def insert(self, name, code, category, market):
        obj = Company(name, code, category, market)
        obj = self._insert(obj)
        return obj.id
    
        



    