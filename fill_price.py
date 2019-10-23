#-*- coding: utf-8 -*-
import os
import json
import logging

from common.logger import LogCfg
from common.appctx import AppContext

log = logging.getLogger("qi.fill_price")

def get_ctx():
    cur_path = os.path.dirname(__file__)
    ctx_path = os.path.join(cur_path, "ctx.json")
    with open(ctx_path, "r") as f:
        data = f.read()
    return json.loads(data)

ctx = get_ctx()
app_ctx = AppContext(ctx)

def main():
    price_data = app_ctx.get_bean("price_data")
    price_data.fill_price()

if __name__ == "__main__":
    main()
