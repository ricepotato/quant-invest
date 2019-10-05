#-*- coding: utf-8 -*-
import datetime
import logging

log = logging.getLogger("qi.data.calc")

class CalcException(Exception):
    pass

class DateRangeError(CalcException):
    pass

class DateCalc:
    def __init__(self, st_date):
        self.st_date = st_date
        self._split()

    def _split(self):
        date_list = self.st_date.split("-")
        self.year = int(date_list[0])
        self.month = int(date_list[1])

    def __lt__(self, other) -> bool:
        if self > other:
            return False
        elif self == other:
            return False
        else:
            return True

    def __eq__(self, other) -> bool:
        if self.st_date == other.st_date:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        if self.year < other.year:
            return False
        elif self.year == other.year:
            if self.month > other.month:
                return True
            else:
                return False
        else:
            return True

    def __add__(self, val: int):
        month = self.month + val
        year = self.year
        while month > 12:
            year += 1
            month -= 12

        return DateCalc("{}-{:02}".format(year, month))

    def __repr__(self):
        return self.st_date

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DateRangeError as e:
            log.error("get result error. %s", e)
            return {"code":args[1], "error":str(e)}
    return wrapper

class Calc:
    def __init__(self):
        self.price_data = None

    @handle_exception
    def get_result(self, code: str, st_date: str, 
                 hold: int, period: int) -> dict:
        """ code : 종목코드 st_date : 시작 년 월(yyyy-dd)
        hold : 보유기간, period : 전체기간
        """
        self._validate(st_date, hold, period)
        st = DateCalc(st_date)
        total = self._get_item(code, str(st), str(st + period))
        res = {
            "code":code,
            "total":total
        }
        er_list = []
        
        for idx in range(period - hold + 1):
            end = st + hold
            item = self._get_item(code, str(st), str(end))
            er_list.append(item)
            st = st + 1
        res["er_list"] = er_list

        total_er = 0
        for item in er_list:
            total_er += item["earning_ratio"]
        if len(er_list) > 0:
            avg_er = float(total_er) / float(len(er_list))
            res["avg_er"] = avg_er
        else:
            res["avg_er"] = 0

        return res

    def _validate(self, st_date, hold, period):
        """ 날짜와 보유기간, 전체기간의 유효성을 검증합니다. """
        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m")
        if DateCalc(st_date) > DateCalc(now_date):
            raise DateRangeError(f"st_date ({st_date}) is later than now ({now_date})")
        if period < hold:
            raise DateRangeError(f"hold ({hold}) must less than period({period})")
        if DateCalc(st_date) + period > DateCalc(now_date):
            raise DateRangeError(f"st_date + period({str(DateCalc(st_date) + period)})"
                                 f" is later than now({now_date})")

    def _get_item(self, code, st_date, end_date):
        st_price = self.price_data.get_price(code, st_date)
        end_price = self.price_data.get_price(code, end_date)
        buy_price = st_price["close"]
        sell_price = end_price["close"]
        er = self._get_er(buy_price, sell_price)

        return {
            "buy":{
                "price":st_price["close"],
                "date":st_price["date"],
                "st_date":st_date
            },
            "sell":{
                "price":end_price["close"],
                "date":end_price["date"],
                "end_date":end_date
            },
            "earning_ratio":er
        }

    def _get_er(self, buy_price, sell_price):
        """ 수익률 계산 """
        earn = sell_price - buy_price
        return float(earn) / float(buy_price) * 100.0
