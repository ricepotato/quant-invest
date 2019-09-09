
import FinanceDataReader as fdr

class PriceData:
    
    def __init__(self):
        self.comp_dao = None
        self.price_dao = None

    def fill_price(self):
        comp_list = self.comp_dao.select()

    def get_df(self, code: str):
        """ get data field 
        KeyError: '2014-02-02 00:00:00'
        >>> 
        >>> df.loc["2014-02-03 00:00:00"].Open
        38144.0
        >>> df.loc["2014-02-03 00:00:00"]
        Open       38144.000000
        High       38577.000000
        Low        37626.000000
        Close      37889.000000
        Volume    426267.000000
        Change        -0.021209
        Name: 2014-02-03 00:00:00, dtype: float64
        >>> 
        """
        df = fdr.DataReader(code, "2014-01-01")
        #df.loc["2014-{"]
