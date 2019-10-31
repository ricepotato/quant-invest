
from qi.database import DBFactory
from schemas import FinancialReport, Company, Market

class StockDao:
    def __init__(self):
        self.db = DBFactory.from_conf("conf/database.ini")

    def get_data(self, market, **kwargs):
        with self.db.session_scope() as s:
            q = s.query(Company, FinancialReport)
            q = q.filter(Company.id == FinancialReport.comp_id)
            q = q.filter(Market.id == Company.market)
            q = q.filter(Market.name == market)
            year = kwargs.get("year", None)
            min_mrkcap = kwargs.get("min_mrkcap", None)
            if year is not None:
                q = q.filter(FinancialReport.period.like(f"{year}%"))
            if min_mrkcap is not None:
                q = q.filter(Company.market_cap > min_mrkcap)
            
            rs_func = lambda item: {"code":item[0].code, 
                                    "market_cap":item[0].market_cap,
                                    "company_name":item[0].name,
                                    "period":item[1].period,
                                    "roa":item[1].roa, "roe":item[1].roe,
                                    "per":item[1].per, "pbr":item[1].pbr,
                                    "date_insert":item[1].date_insert}
            return list(map(rs_func, q))
