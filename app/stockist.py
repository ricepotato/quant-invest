# -*- coding: utf-8 -*-
import logging

from app.data.screader import SCReader
from app.database.dao import MongoDao


log = logging.getLogger("qi.stockist")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

dao = MongoDao()


def insert(filepath, market):
    reader = SCReader()
    kosdaq_res = reader.read_file(filepath)

    for item in kosdaq_res:
        item["market"] = market
        # obj = coll.find_one({"code": item["code"]})
        obj = dao.find_by_code(item["code"])
        if obj:
            log.info("item already exist code=%s", item["code"])
            continue
        # coll.insert_one(item)
        dao.insert(item)
        log.info("insert one %s", item["name"])


def main():
    insert("data/KOSDAQ_2020.csv", "KOSDAQ")
    insert("data/KOSPI_2020.csv", "KOSPI")


if __name__ == "__main__":
    main()
