#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, FLOAT, DATETIME
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

cur_path = os.path.dirname(__file__)
comm_path = os.path.join(cur_path, "..")

sys.path.append(comm_path)

log = logging.getLogger("qi.common.database")

def get_conf(conf_path=None):
    """ json 설정 파일을 읽어온다.
    기본 설정파일 경로는 파일경로/database.conf
    설정 파일 경로를 지정하지 않으면 기본 파일경로에서 읽어온다.

    @param conf_path : str
    @return : dict
    """
    log.debug("reading conf file...")
    if conf_path is None:
        conf_path = os.path.join(cur_path, "database.conf")
    
    log.debug("conf_path=%s", conf_path)
    try:
        with open(conf_path, "r") as f:
            conf_data = f.read()
        cfg = json.loads(conf_data)
    except IOError as e:
        log.error("get config io error. %s", e)
        return None
    except ValueError as e:
        log.error("get config value error. %s", e)
        return None
    return cfg
 
cfg = get_conf()

conn_str = "mysql://{}:{}@{}:{}/{}?charset=utf8".format(cfg["user"], cfg["password"], 
                                           cfg["host"], cfg["port"], cfg["database"])
Base = declarative_base()
engine = create_engine(conn_str, convert_unicode=False, echo=False) 

class Dictionary(dict):
    
    def __getattr__(self, key):
        return self[key]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Serializer(object):
    obj_map = {}

    def _make_dict(self, attr):
        if isinstance(attr, Base):
            res = self.obj_map.get(id(attr), None)
            if not res:
                return attr.to_dict()
            else:
                return res
        if isinstance(attr, list):
            res = []
            for item in attr:
                res.append(self._make_dict(item))

        return attr

    def to_dict(self):
        ret = Dictionary()
        self.obj_map[id(self)] = ret
        for key in inspect(self).attrs.keys():
            ret[key] = self._make_dict(getattr(self, key))

        return ret


# 시장 구분 용도
class Market(Base, Serializer):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True) # pkey
    name = Column(String(10)) # KOSDAQ, KOSPI

    UniqueConstraint(name, name="unique_name")

    __table_args__ = {'mysql_engine':'InnoDB', 
                      'mysql_charset':'utf8', 
                      'mysql_collate':'utf8_general_ci'}

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Market('%s')>" % (self.name)

# 업종
class Category(Base, Serializer):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True) # pkey
    code = Column(String(20)) # 업종코드
    description = Column(String(100)) # 업종이름 ex)영화, 비디오물, 방송프로그램 제작 및 배급업

    UniqueConstraint(code, name="unique_cate_code")

    __table_args__ = {'mysql_engine':'InnoDB', 
                      'mysql_charset':'utf8', 
                      'mysql_collate':'utf8_general_ci'}

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __repr__(self):
        return "<Category('%s', '%s')>" % (self.code, self.description)

class Company(Base, Serializer):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True) # pkey
    name = Column(String(50)) # 종목명
    code = Column(String(20)) # 종목 코드
    category = Column(Integer, ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"))
    market = Column(Integer, ForeignKey("market.id", ondelete="CASCADE", onupdate="CASCADE"))

    UniqueConstraint(name, code, name="unique_name")
    #UniqueConstraint(code, name="unique_code")
    #Index("name_idx", name)
    #Index("code_idx", code)

    __table_args__ = {'mysql_engine':'InnoDB', 
                      'mysql_charset':'utf8', 
                      'mysql_collate':'utf8_general_ci'}

    def __init__(self, name, code, category, market):
        self.name = name
        self.code = code
        self.category = category
        self.market = market

    def __repr__(self):
        return "<Stock('%s', '%s')>" % (self.name, self.code)


class FinancialReport(Base, Serializer):
    __tablename__ = "fr"

    id = Column(Integer, primary_key=True) # pkey
    comp_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"))
    period = Column(String(10))
    per = Column(FLOAT)
    pbr = Column(FLOAT)
    roa = Column(FLOAT)
    roe = Column(FLOAT)
    evebita = Column(FLOAT) # ev/evita
    marketcap = Column(Integer) # 시가총액
    date_insert = Column(DATETIME)

    Index("per_idx", per)
    Index("pbr_idx", pbr)
    Index("roa_idx", roa)
    Index("roe_idx", roe)

    __table_args__ = {'mysql_engine':'InnoDB', 
                      'mysql_charset':'utf8', 
                      'mysql_collate':'utf8_general_ci'}

    def __init__(self, comp_id, period, per, pbr, roa, roe, evebita, marketcap, date_insert):
        self.comp_id = comp_id
        self.period = period
        self.per = per
        self.pbr = pbr
        self.roa = roa
        self.roe = roe
        self.evebita = evebita
        self.marketcap = marketcap
        self.date_insert = date_insert

    def __repr__(self):
        return "<FinancialReport('%d', '%d')>" % (self.id, self.comp_id)

class Singleton(type):
    """Singleton.
    @see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.engine = engine
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)

    def __del__(self):
        """Disconnects pool."""
        self.engine.dispose()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            log.error("Database Error. %s", e)
            session.rollback()
        finally:
            session.close()

    def create_all(self):
        try:
            Base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to create or connect to database: %s", e)

    def drop_all(self):
        """Drop all tables."""
        try:
            Base.metadata.drop_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to drop all tables of the database: %s", e)
