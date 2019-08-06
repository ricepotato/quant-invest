#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

log = logging.getLogger('qi.server.server')

from flask import Flask, jsonify, got_request_exception, request
from flask_restful import Resource, Api
from exc import *

class APIServer(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.errors = {
            "NoContent":{
                "message":"No Content",
                "status":204
            },
            "BadRequest":{
                "message":"Bad Request",
                "status":400
            }
        }

        self.api = Api(self.app, errors=self.errors, catch_all_404s=True)
        got_request_exception.connect(self._log_exception, self.app)

    def run(self, port=8080, host="0.0.0.0", debug=False):
        self.app.run(port=port, host=host, debug=debug)

    def add_resource(self, *args, **kwargs):
        self.api.add_resource(*args, **kwargs)

    def _log_exception(self, sender, exception, **extra):
        log.exception("exception=%s, method=%s, url=%s, values=%s",
                        exception, request.method, request.url, request.values)
