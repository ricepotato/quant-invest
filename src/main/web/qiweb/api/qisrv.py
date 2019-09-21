#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from .base import APIBase

class QIApi(APIBase):
    def __init__(self):
        APIBase.__init__(self)
        self.from_conf_file("qi-server")

    def get_stock(self, market, year):
        resource = f"stock/{market}/{year}"
        return self.get(resource)

