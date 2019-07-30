
import os
import sys
import logging

cur_path = os.path.dirname(__file__)
comm_path = os.path.join(cur_path, "..")

sys.path.append(comm_path)

from database.database import *
import logger.logcfg

log = logging.getLogger("qi.common.database.stock_dao")

from database import *

def to_dict(item):
    return {
        "comp_code":item[0].code,
        "comp_name":item[0].name, "roe":item[1].roe,
        "roa":item[1].roa, "roe":item[1].roe,
        "per":item[1].per, "pbr":item[1].pbr, 
        "evebita":item[1].evebita, "marketcap":item[1].marketcap,
        "date_insert":item[1].date_insert
    }

class StockDao(object):
    
    def __init__(self, db):
        self.db = db

    def get_list(self, market, period, params={}):
        with self.db.session_scope() as s:
            obj = s.query(Market).filter(Market.name==market).first()
            if not obj:
                log.debug("market not exist. %s", market)
                return None
            
            q = s.query(Company, FinancialReport)
            q = q.filter(FinancialReport.comp_id == Company.id)
            q = q.filter(Company.market == obj.id)
            q = q.filter(FinancialReport.period == period)

            res = list(map(to_dict, q.all()))
            return res

            