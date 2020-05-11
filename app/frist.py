# -*- coding: utf-8 -*-
import logging

from app.database.dao import MongoDao
from app.data.crawler import CompGuideCrawler


log = logging.getLogger("qi.frist")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

filelog = logging.getLogger("parseerror")
filelog.addHandler(logging.FileHandler("data/parseerror.log"))
filelog.setLevel(logging.INFO)


dao = MongoDao()


def insert_data(code, data):
    log.info("insert data code=%s", code)
    dao.set_object(code, {"market_cap": data["market_cap"]})
    dao.set_object(code, {"fr": data["period"]})


def frist(market):
    kosdaq_list = dao.get_stock_list(market)
    kosdaq_code_map = map(lambda item: item["code"], kosdaq_list)
    for code in kosdaq_code_map:

        if dao.exist(code, "fr"):
            log.info("fr object exist. code=%s", code)
            continue

        crawler = CompGuideCrawler()
        log.info("getting fr code=%s", code)
        try:
            data = crawler.get_fr_data(code)
        except IndexError as e:
            log.error("parse error. %s", e)
            filelog.info("%s", code)
            continue

        insert_data(code, data)


def main():
    frist("KOSDAQ")
    frist("KOSPI")


if __name__ == "__main__":
    main()
