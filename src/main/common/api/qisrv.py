#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from .base import APIBase

class QIApi(APIBase):
    def __init__(self):
        APIBase.__init__(self)
        self.from_conf_file("qi-server")

    def get_stock(self, market, year, min_mrkcap):
        resource = f"stock/{market}/{year}"
        params = {"min_mrkcap":min_mrkcap}
        return self.get(resource, params)

