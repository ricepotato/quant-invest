# -*- coding: utf-8 -*-
import logging

from app.data.screader import SCReader
from app.database.mongo import get_db


log = logging.getLogger("qi")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

db = get_db()
qi = db["qi"]
coll = qi.stock

def insert(filepath, market):
    reader = SCReader()
    kosdaq_res = reader.read_file(filepath)

    for item in kosdaq_res:
        item["market"] = market
        obj = coll.find_one({"code": item["code"]})
        if obj:
            log.info("item already exist code=%s", item["code"])
            continue
        coll.insert_one(item)
        log.info("insert one %s", item["name"])

def main():
    insert("data/KOSDAQ_2020.csv", "KOSDAQ")
    insert("data/KOSPI_2020.csv", "KOSPI")


if __name__ == "__main__":
    main()
