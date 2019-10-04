#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

log = logging.getLogger('qi.server.resource.erboard')

from flask import jsonify
from flask_restful import Resource, reqparse

class ERBoard(Resource):
    """ 수익률 자원 """
    def __init__(self, **kwargs):
        self.er_data = kwargs["er_data"]

    def get(self, group=None):
        """ get method 호출시 """
        args = self._parse_req()
        res = {"msg":"erboard get"}
        return jsonify(res)

    def _parse_req(self):
        parser = reqparse.RequestParser()
        parser.add_argument("min_roa", type=float)
        parser.add_argument("min_per", type=float)
        parser.add_argument("min_mrkcap", type=int)
        parser.add_argument("limit", type=int)
        args = parser.parse_args()
        return args

    def post(self):
        pass
