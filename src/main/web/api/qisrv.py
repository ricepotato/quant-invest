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

    def get_er(self, group=None):
        if group is None:
            resource = "er"
        else:
            resource = f"er/{group}"
        return self.get(resource)

    def post_er(self, code, st_date, hold, period, group=None):
        resource = "er"
        data = {"code":code, "st_date":st_date, 
                "hold":hold, "period":period}
        if group is not None:
            data["group"] = group
        return self.post(resource, data=data)

    def delete_er(self, id):
        resource = f"er/{id}"
        return self.delete(resource)


