from dataclasses import dataclass


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

