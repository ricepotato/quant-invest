#-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String, 
                        FLOAT, DATETIME, SMALLINT)
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.schema import ForeignKey

Base = declarative_base()

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
    market_cap = Column(Integer)
    market = Column(Integer, ForeignKey("market.id", ondelete="CASCADE", onupdate="CASCADE"))
    

    UniqueConstraint(name, code, name="unique_name")
    Index("market_cap_idx", market_cap)
    Index("market_idx", market)
    Index("code_idx", code)

    __table_args__ = {'mysql_engine':'InnoDB', 
                      'mysql_charset':'utf8', 
                      'mysql_collate':'utf8_general_ci'}

    def __init__(self, name, code, category, market_cap, market):
        self.name = name
        self.code = code
        self.category = category
        self.market_cap = market_cap
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

    UniqueConstraint(comp_id, period, name="unique_comp_id_period")
    Index("per_idx", per)
    Index("pbr_idx", pbr)
    Index("roa_idx", roa)
    Index("roe_idx", roe)
    Index("period_idx", period)

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

class Price(Base, Serializer):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True) # pkey
    code = Column(String(20)) # 종목 코드
    date = Column(String(10), nullable=False)
    open = Column(Integer) # 시가
    high = Column(Integer) # 고가
    low = Column(Integer) # 저가
    close = Column(Integer) # 종가
    volume = Column(Integer) # 거래량
    change = Column(Integer) # 등락

    UniqueConstraint(code, date, name="unique_code_date")

    def __init__(self, code, date, open, high, low, close, volume, change):
        self.code = code
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.change = change

    def __repr__(self):
        return "<Price('%s', '%s')>" % (self.code, str(self.close))

class ERBoard(Base, Serializer):
    __tablename__ = "er_board"

    id = Column(Integer, primary_key=True) # pkey
    code = Column(String(20)) # 종목 코드
    st_date = Column(String(10), nullable=False) # 시작 날짜
    hold = Column(SMALLINT, nullable=False) # 보유기간
    period = Column(SMALLINT, nullable=False) # 전체기간
    group = Column(SMALLINT) # group

    Index("group_idx", group)
    
    def __init__(self, code: str, st_date: str, hold: int, period: int, 
                 group: int=None) -> int:
        self.code = code
        self.st_date = st_date
        self.hold = hold
        self.period = period
        self.group = group

    def __repr__(self):
        return "<ERBoard('%s')>" % (self.code)