#-*- coding: utf-8 -*-

import logging

log = logging.getLogger("qi.data.calc")

class DateCalc:
    def __init__(self, st_date):
        self.st_date = st_date

    def add(self, val):
        """ 날짜 계산기 val 값만큼 더한 월까지의 날짜 문자열을 구함 """
        date_list = self.st_date.split("-")
        year = int(date_list[0])
        month = int(date_list[1])

        month += val
        while month > 12:
            year += 1
            month -= 12

        return "{}-{:02}".format(year, month)

    def __add__(self, other: int):
        return DateCalc(self.add(other))

    def __repr__(self):
        return self.st_date

class Calc:
    def __init__(self):
        self.price_data = None

    def get_list(self, code: str, st_date: str, 
                 hold: int, period: int) -> dict:

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

    def _get_item(self, code, st_date, end_date):
        st_price = self.price_data.get_price(code, st_date)
        end_price = self.price_data.get_price(code, end_date)
        buy_price = st_price["close"]
        sell_price = end_price["close"]
        st_datetime = st_price["date"]
        end_datetime = end_price["date"]
        er = self._get_er(buy_price, sell_price)

        return {"st":st_date, "st_datetime":st_datetime,
                "end_datetime":end_datetime, "end":end_date,
                "buy_price":buy_price, "sell_price":sell_price,
                "earning_ratio":er}

    def _get_er(self, buy_price, sell_price):
        """ 수익률 계산 """
        earn = sell_price - buy_price
        return float(earn) / float(buy_price) * 100.0
