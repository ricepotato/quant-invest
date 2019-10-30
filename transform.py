#-*- coding: utf-8 -*-
import os
import sys
import logging

import qi.logger.logcfg
from qi.appctx import AppContext
from multiprocessing import Pool

log = logging.getLogger("qi.transform")
log.setLevel(logging.DEBUG)

ctx = {
    "db":{
        "class":"qi.database.Database"
    },
    "fr_dao":{
        "class":"qi.database.FinancialReportDao",
        "init_args":[{"bean":"db"}]
    },
    "company_dao":{
        "class":"qi.database.CompanyDao",
        "init_args":[{"bean":"db"}]
    },
    "category_dao":{
        "class":"qi.database.CategoryDao",
        "init_args":[{"bean":"db"}]
    },
    "mrk_dao":{
        "class":"qi.database.MarketDao",
        "init_args":[{"bean":"db"}]
    },
    "collector":{
        "class":"data.FrCollector",
        "init_args":[
            {"bean":"store"}, {"bean":"frdata"}
        ]
    },
    "store":{
        "class":"data.StockDbStore",
        "init_args":[
            {"bean":"mrk_dao"}, {"bean":"category_dao"},
            {"bean":"company_dao"}, {"bean":"fr_dao"}
        ]
    },
    "frdata":{
        "class":"data.CompanyGuideFrData",
        "init_args":[
            {"bean":"crawler"}
        ]
    },
    "crawler":{
        "class":"crawler.CompGuideCrawler"
    },
    "transform":{
        "class":"crawler.transform.Transform",
        "properties":{
            "crawler":{"bean":"crawler"}
        }
    }
}

app_ctx = AppContext(ctx)

def transform_run(comp_code):
    transform = app_ctx.get_bean("transform")
    transform.transfrom(comp_code)

def main():
    log.info("transform run")
    transform = app_ctx.get_bean("transform")
    comp_dao = app_ctx.get_bean("company_dao")

    res = comp_dao.select()
    code_list = list(map(lambda item: item["code"], res))
    cnt = 0
    total = len(code_list)
    with Pool(20) as p:
        p.map(transform_run, code_list)

    #transform_run("263020")

if __name__ == "__main__":
    main()