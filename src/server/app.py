#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.append(base_path)

log = logging.getLogger('qi.server.app')

from server import APIServer
from resources.stock import Stock
from common.appctx import AppContext

ctx = {
    "dao":{
        "class":"server.dao.StockDao"
    },
    "rank":{
        "class":"data.rank.Rank"
    },
    "stock_db":{
        "class":"server.data.StockDbData",
        "properties":{
            "dao":{"bean":"dao"},
            "rank":{"bean":"rank"}
        }
    }
}
app_ctx = AppContext(ctx)
app_ctx.get_bean("stock_db")
st_data = app_ctx.get_bean("stock_db")
rck = {"st_data":st_data}

server = APIServer()
app = server.app
api.add_resource(Stock, "/stock/<string:market>/<string:year>", 
                     resource_class_kwargs=rck)

def main():
    server.run(port=8091)

if __name__ == "__main__":
    main()