#-*- coding: utf-8 -*-

import logging
import configparser
import importlib

from sqlalchemy import create_engine

from .database import Database

log = logging.getLogger("qi.database.factory")

class DBFactory:
    @staticmethod
    def from_conf(conf_path):
        config = configparser.ConfigParser()
        config.read(conf_path)
        db_sec = config["database"]

        mod = importlib.import_module(db_sec["schema"])
        Base = getattr(mod, "Base")

        conn_str = "mysql://{}:{}@{}:{}/{}?charset=utf8".format(
            db_sec["user"], db_sec["password"], db_sec["host"], 
            db_sec["port"], db_sec["db"])
        engine = create_engine(conn_str, convert_unicode=False, echo=False)
        return Database(Base, engine)


        