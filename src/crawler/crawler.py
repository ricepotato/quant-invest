#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))
#comm_path = os.path.abspath(os.path.join(cur_path, "..", "common"))

sys.path.append(base_path)

import common.logger.logcfg

log = logging.getLogger("qi.crawler.crawler")

class Crawler(object):
    def __init__(self):
        pass

    def start(self):
        log.info("crawler start.")

    def _get_data(self, comp_code):
        """ 종목코드 입력 시 roe, roa, per, pbr 값을 가져와 return 한다.
        return 값의 period 는 
        @param comp_com : str
        @return : dict
        """ 
        return {"comp_code":comp_code, "period":"2018/12", "roe":0, "roa":0, "per":0, "pbr":0}

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()