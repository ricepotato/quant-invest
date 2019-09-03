import os
import sys
import logging

from common.logger import LogCfg
from common.appctx import AppContext

log = logging.getLogger("qi.transform")
log.setLevel(logging.DEBUG)

ctx = {
    "db":{
        "class":"common.database.Database"
    },
    "fr_dao":{
        "class":"common.database.FinancialReportDao",
        "init_args":[{"bean":"db"}]
    },
    "company_dao":{
        "class":"common.database.CompanyDao",
        "init_args":[{"bean":"db"}]
    },
    "category_dao":{
        "class":"common.database.CategoryDao",
        "init_args":[{"bean":"db"}]
    },
    "mrk_dao":{
        "class":"common.database.MarketDao",
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

def main():
    log.info("transform run")
    transform = app_ctx.get_bean("transform")
    comp_dao = app_ctx.get_bean("company_dao")

    res = comp_dao.select()
    code_list = list(map(lambda item: item["code"], res))
    cnt = 0
    total = len(code_list)
    for code in code_list:
        log.info("trasnform code=%s (%d/%d)", code, cnt, total)
        cnt += 1
        transform.transfrom(code)

if __name__ == "__main__":
    main()