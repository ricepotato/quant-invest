#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

import common.logger.logcfg

log = logging.getLogger('qi.server.stock')

try:
    from flask import jsonify
    from flask_restful import Resource, reqparse
except ImportError as e:
    log.error("import error. install flask 'pip install flask'")

class Stock(Resource):
    """ 주식정보 자원 """
    def __init__(self, **kwargs):
        self.stock_data = kwargs["st_data"]

    def get(self, market=None):
        """ get method 호출시 """
        args = self._parse_req()        
        res = {"stock":self.stock_data.get_data(market, args), "market":market}
        return jsonify(res)

    def _parse_req(self):
        parser = reqparse.RequestParser()

        parser.add_argument("min_roa", type=float)
        parser.add_argument("min_per", type=float)
        parser.add_argument("min_mrkcap", type=int)
        parser.add_argument("limit", type=int)
        args = parser.parse_args()
        return args
        
