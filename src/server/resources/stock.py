#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

log = logging.getLogger('qi.server.resource.stock')


from flask import jsonify
from flask_restful import Resource, reqparse

class Stock(Resource):
    """ 주식정보 자원 """
    def __init__(self, **kwargs):
        self.stock_data = kwargs["st_data"]

    def get(self, market: str, year: str):
        """ get method 호출시 """
        args = self._parse_req()
        kwargs = self._stock_data_kwargs(args)
        kwargs["year"] = year
        res = {"stock_list":self.stock_data.get_data(market, **kwargs),
               "market":market}
        return jsonify(res)

    def _parse_req(self):
        parser = reqparse.RequestParser()
        parser.add_argument("min_roa", type=float)
        parser.add_argument("min_per", type=float)
        parser.add_argument("min_mrkcap", type=int)
        parser.add_argument("limit", type=int)
        args = parser.parse_args()
        return args

    def _stock_data_kwargs(self, args) -> dict:
        """ args 로 kwargs dict 를 만들어냄.
        args 값이 없는 경우 kwargs 에서 제외함. """
        kwargs = {}
        for key in ["limit", "min_mrkcap"]:
            val = getattr(args, key)
            if val is not None:
                kwargs[key] = val

        return kwargs

        
