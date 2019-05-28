#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

from sqlalchemy import create_engine, Column, Integer, String, FLOAT
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base



cur_path = os.path.dirname(__file__)
comm_path = os.path.join(cur_path, "..")

sys.path.append(comm_path)

import logger.logcfg

log = logging.getLogger("qi.common.database")
log.setLevel(logging.DEBUG)

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
engine = create_engine(conn_str, convert_unicode=False) 

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True) # pkey
    name = Column(String(50)) # 종목명
    code = Column(String(20)) # 종목 코드

    UniqueConstraint(name, code, name="unique_name")
    #UniqueConstraint(code, name="unique_code")
    #Index("name_idx", name)
    #Index("code_idx", code)

    #__table_args__ = {""}

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return "<Stock('%s', '%s')>" % (self.name, self.code)


class FinancialReport(Base):
    __tablename__ = "fr"

    id = Column(Integer, primary_key=True) # pkey
    comp_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"))
    period = Column(String(10))
    per = Column(FLOAT)
    pbr = Column(FLOAT)
    roa = Column(FLOAT)
    roe = Column(FLOAT)
    marketcap = Column(Integer) # 시가총액

    Index("per_idx", per)
    Index("pbr_idx", pbr)
    Index("roa_idx", roa)
    Index("roe_idx", roe)

    def __init__(self, comp_id):
        self.code = comp_id

    def __repr__(self):
        return "<Stock('%d', '%d')>" % (self.id, self.comp_id)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
