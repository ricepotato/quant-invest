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
    from flask import Flask, jsonify
    from flask_restful import Resource, Api
except ImportError as e:
    log.error("import error. install flask 'pip install flask'")

class Stock(Resource):
    """ 주식정보 자원 """

    def get(self, market=None):
        """ get method 호출시 """
        res = {"success":True, "msg":"stock select", "market":market}
        return jsonify(res)

    def post(self):
        res = {"success":True, "msg":"stock insert"}
        return jsonify(res)
