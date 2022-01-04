from typing import List
from dataclasses import dataclass


@dataclass
class FinancialReport:
    def __init__(
        self, code: str, period: str, roa: float, roe: float, per: float, pbr: float
    ):
        self.code = code
        self.period = period
        self.roa = roa
        self.roe = roe
        self.per = per
        self.pbr = pbr

    def __eq__(self, other):
        return self.code == other.code and self.period == other.period


@dataclass
class Stock:
    def __init__(
        self,
        code: str,
        name: str,
        market: str,
        category_code: str = None,
        desc: str = None,
        market_cap: int = None,
    ):
        self.code = code
        self.name = name
        self.market = market
        self.category_code = category_code
        self.desc = desc
        self.market_cap = market_cap
        self.fr: dict = {}

    @classmethod
    def from_dict(cls, obj: dict):
        stock = cls(obj["code"], obj["name"], obj["market"])
        if obj.get("category_code"):
            stock.category_code = obj["category_code"]
        if obj.get("desc"):
            stock.desc = obj["desc"]
        if obj.get("market_cap"):
            stock.market_cap = obj["market_cap"]
        if obj.get("fr"):
            for period, fr_item in obj.get("fr").items():
                stock.fr[period] = FinancialReport(
                    obj["code"],
                    period,
                    fr_item["roa"],
                    fr_item["roe"],
                    fr_item["per"],
                    fr_item["pbr"],
                )

        return stock

    def to_dict(self):
        result = {"code": self.code, "name": self.name, "market": self.market}
        if self.category_code:
            result["category_code"] = self.category_code
        if self.desc:
            result["desc"] = self.desc
        if self.market_cap:
            result["market_cap"] = self.market_cap

        if self.fr:
            fr = {}
            for period, fr_item in self.fr.items():
                fr[period] = {
                    "roa": fr_item.roa,
                    "roe": fr_item.roe,
                    "per": fr_item.per,
                    "pbr": fr_item.pbr,
                }
            result["fr"] = fr

        return result
