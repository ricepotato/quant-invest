
import os

cur_path = os.path.dirname(__file__)
comm_path = os.path.join(cur_path, "..")

sys.path.append(comm_path)

import logger.logcfg

log = logging.getLogger("qi.common.database.stock_dao")

from database import *

class StockDao(object):
    
    def __init__(self, db):
        self.db = db

    def get_list(self, market, period):

        with self.db.session_scope() as s:
            obj = s.query(Market).filter(Market.name=market).first()
            if not obj:
                log.debug("market not exist. %s", market)
                return None
            
            q = s.query(Company, FinancialReport)
            q = q.filter(FinancialReport.comp_id == Company.id)
            q = q.filter(Company.market == obj.id)
            q = q.filter(FinancialReport.period == period)
            
            