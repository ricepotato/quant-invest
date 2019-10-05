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

    def get(self, id=None):
        """ get method 호출시 """
        res = self.er_data.get(group=id)
        return jsonify(res)

    def post(self):
        args = self._parse_req()
        data = {"code":args.code, "st_date":args.st_date, 
                "hold":args.hold, "period":args.period}
        id = self.er_data.add(data)
        res = {"id":id}
        return jsonify(res)

    def delete(self, id):
        count = self.er_data.delete(id=id)
        res = {"count":count}
        return jsonify(res)

    def _parse_req(self):
        parser = reqparse.RequestParser()
        parser.add_argument("st_date", type=str, required=True)
        parser.add_argument("code", type=str, required=True)
        parser.add_argument("hold", type=int, required=True)
        parser.add_argument("period", type=int, required=True)
        args = parser.parse_args()
        return args