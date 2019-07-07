#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

import logger.logcfg

log = logging.getLogger("qi.data.reader")


class SCReader(object):
    """ Stock csv reader """
    def __init__(self):
        pass

    def from_file(self, path):
        log.debug("reading file. path=%s", path)
        with open(path, "rt", encoding="UTF8") as f:
            data = f.read()
        return data

    def _validate(self, col_list):
        num = int(col_list[0])
        if len(col_list[1]) != 6:
            raise ValueError("code value length erorr.")
        if len(col_list[3]) != 6:
            raise ValueError("cate code value length erorr.")

    def _get_col(self, col_list):
        self._validate(col_list)
        num = int(col_list[0])
        code = col_list[1]
        name = col_list[2]
        cate_code = col_list[3]
        
        return {"num":num, "code":code, "name":name, 
                "category_code":cate_code}

    def parse(self, data):
        
        res = []
        log.debug("parsing..")
        for line in data.split("\n"):
            col_list = line.split(",")
            try:
                res.append(self._get_col(col_list))
            except ValueError as e:
                log.warning("_get_col value error. %s line=%s", e, line)
                continue

        return res

    def read_file(self, path):
        data = self.from_file(path)
        res = self.parse(data)
        return res