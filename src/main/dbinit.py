#-*- coding: utf-8 -*-
import os
import sys
import logging

from common.logger import LogCfg
from common.database.database import Database
from common.database.dao import *

log = logging.getLogger("qi.data.dbinit")

def init_database():
    Database().drop_all()
    Database().create_all()

def main():
    log.info("dbinit main.")
    init_database()

if __name__ == "__main__":
    main()