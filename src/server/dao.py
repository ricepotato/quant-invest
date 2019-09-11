
from common.database import Database, Company, Market, FinancialReport

class StockDao:
    def __init__(self):
        self.db = Database()

    def get_data(self, market, **kwargs):
        with self.db.session_scope() as s:
            q = s.query(Company, FinancialReport)
            q = q.filter(Company.id == FinancialReport.comp_id)
            q = q.filter(Market.id == Company.market)
            q = q.filter(Market.name == market)
            year = kwargs.get("year", None)
            if year is not None:
                q = q.filter(FinancialReport.period.like(f"{year}%"))
            
            #q = q.limit(10)
            rs_func = lambda item: {"code":item[0].code, 
                                    "company_name":item[0].name, 
                                    "fr":item[1].to_dict()}
            return list(map(rs_func, q))
