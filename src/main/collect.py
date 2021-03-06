import os
import sys
import logging

from common.logger import LogCfg
from common.appctx import AppContext

log = logging.getLogger("qi.main")
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
        ],
        "properties":{
            "json_reader":{"bean":"json_reader"}
        }
    },
    "crawler":{
        "class":"crawler.CompGuideCrawler"
    },
    "json_reader":{
        "class":"crawler.reader.CompJsonReader"
    }
}

app_ctx = AppContext(ctx)

def main():
    log.info("main run")
    collector = app_ctx.get_bean("collector")
    collector.collect("KOSPI")
    collector.collect("KOSDAQ")

if __name__ == "__main__":
    main()