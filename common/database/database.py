#-*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, FLOAT
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://qi:password@127.0.0.1:3307/qi?charset=utf8', 
                        convert_unicode=False) 

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
