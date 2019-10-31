#-*- coding: utf-8 -*-
import os
import sys
import json
import logging
import csv

log = logging.getLogger("qi.data.reader")

class SCReader(object):
    """ Stock csv reader 
    주식정보 csv 파일을 읽어 list 로 반환한다. """
    def __init__(self):
        pass

    def from_file(self, path):
        log.debug("reading file. path=%s", path)
        with open(path, "r", encoding="UTF8") as f:
            rdr = csv.reader(f)
            data = list(map(lambda line : line, rdr))
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
        desc = col_list[4]
        
        return {"num":num, "code":code, "name":name, 
                "category_code":cate_code, "desc":desc}

    def parse(self, data):
        
        res = []
        for line in data:
            col_list = line
            try:
                res.append(self._get_col(col_list))
            except ValueError as e:
                log.warning("_get_col value error. %s line=%s", e, line)
                continue
            except IndexError as e:
                log.warning("_get_col Index error. %s line=%s", e, line)
                continue

        return res

    def read_file(self, path):
        data = self.from_file(path)
        res = self.parse(data)
        return res