#-*- coding: utf-8 -*-
import os
import sys
import logging

import qi.logger.logcfg
from qi.database import Database

log = logging.getLogger("qi.data.dbinit")

def init_database():
    Database().drop_all()
    Database().create_all()

def main():
    """ database table 을 삭제하고 새로 생성함 """
    log.info("dbinit main.")
    init_database()

if __name__ == "__main__":
    main()