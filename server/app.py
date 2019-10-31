#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import sys
import logging

from qi.apisrv import APIServer
from qi.appctx import AppContext
from resources.stock import Stock
from resources.er import ERBoard

log = logging.getLogger('qi.server.app')

ctx_json = os.path.join(os.path.dirname(__file__), "ctx.json")
app_ctx = AppContext.from_jsonfile(ctx_json)
st_data = app_ctx.get_bean("stock_db")
er_data = app_ctx.get_bean("er_data")
rck = {"st_data":st_data, "er_data":er_data}

server = APIServer()
app = server.app
server.add_resource(Stock, "/stock/<string:market>/<string:year>", 
                    resource_class_kwargs=rck)
server.add_resource(ERBoard, "/er/<int:id>", "/er",
                    resource_class_kwargs=rck)
