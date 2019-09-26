import datetime
import logging
import FinanceDataReader as fdr

log = logging.getLogger("qi.data.price")

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            log.warning("handle exception key error code=%s", args[0])
            return None
    return wrapper

class PriceData:
    
    def __init__(self):
        self.comp_dao = None
        self.price_dao = None
        self.start_year = 2014

    def fill_price(self):
        """ 모든 종가 data 입력 2014 ~ 현재 
        월초, 중순, 하반기 데이터 입력. 종목당 월 3개 항목입력
        """
        comp_list = self.comp_dao.select()
        code_list = map(lambda item: item["code"], comp_list)
        for code in code_list:
            self.get_df(code)

    @handle_exception
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
        df.loc["2014-02"].head(1)
        df.loc["2014-02"].tail(1)

        >>> df.loc["2019-04"].head(1).index[0]
        Timestamp('2019-04-01 00:00:00')

        Open   High    Low  Close  Volume    Change
        """

        # self.start_year 부터 ~ 현재까지
        log.info("get_df code=%s", code)
        df = fdr.DataReader(code, f"{self.start_year}-01-01")
        this_yaer = datetime.datetime.now().year
        for year in range(self.start_year, this_yaer + 1):
            for month in range(1, 13):
                head_df = df.loc["{}-{:02}".format(year, month)].head(1)
                head_dict = self._day_df_to_dict(head_df)
                tail_df = df.loc["{}-{:02}".format(year, month)].tail(1)
                tail_dict = self._day_df_to_dict(tail_df)

                head_dict["code"] = code
                tail_dict["code"] = code

                log.info("add_price date=%s", "{}-{:02}".format(year, month))
                self.price_dao.add_price(head_dict)
                self.price_dao.add_price(tail_dict)

    def _day_df_to_dict(self, df):
        dt = df.index[0]
        date = "{}-{:02}-{:02}".format(dt.year, dt.month, dt.day)
        return {
            "date":date, "open":int(df.Open), "close":int(df.Close),
            "low":int(df.Low), "high":int(df.High), "volume":int(df.Volume),
            "change":float(df.Change)
        }