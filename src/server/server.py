#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

from stock import Stock
import common.logger.logcfg

log = logging.getLogger('qi.server')

try:
    from flask import Flask, jsonify
    from flask_restful import Resource, Api
except ImportError as e:
    log.error("import error. install flask 'pip install flask'")

app = Flask(__name__)

api = Api(app)
api.add_resource(Stock, "/stock", "/stock/<string:market>")

@app.route("/")
def index():
    res = {"success":True, "msg":"hello world"}
    return jsonify(res)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/members")
def members():
    return "Members"

@app.route("/members/<string:name>/")
def getMember(name):
    return name

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)