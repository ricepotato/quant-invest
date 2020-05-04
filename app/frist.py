# -*- coding: utf-8 -*-
import logging

from app.database.dao import MongoDao
from app.data.crawler import CompGuideCrawler


log = logging.getLogger("qi.frist")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

dao = MongoDao()


def insert_data(code, data):
    log.info("insert data code=%s", code)
    dao.set_object(code, {"market_cap": data["market_cap"]})
    dao.set_object(code, {"fr": data["period"]})


def frist(market):
    kosdaq_list = dao.get_stock_list(market)
    kosdaq_code_map = map(lambda item: item["code"], kosdaq_list)
    for code in kosdaq_code_map:

        crawler = CompGuideCrawler()
        data = crawler.get_fr_data(code)
        insert_data(code, data)


def main():
    frist("KOSDAQ")
    frist("KOSPI")


if __name__ == "__main__":
    main()
