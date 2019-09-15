#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import sys
import logging

from resources.stock import Stock
from common.apisrv import APIServer
from common.logger import LogCfg
from common.appctx import AppContext

log = logging.getLogger('qi.server.app')

ctx = {
    "dao":{
        "class":"server.dao.StockDao"
    },
    "rank":{
        "class":"data.rank.Rank"
    },
    "stock_db":{
        "class":"stdata.StockDbData",
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
server.add_resource(Stock, "/stock/<string:market>/<string:year>", 
                     resource_class_kwargs=rck)
