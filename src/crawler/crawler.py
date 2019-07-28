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

class CompGuideCrawler(object):
    """ company guide crawler 
    company guide site 에 방문하여 financial report data 를 가져온다.
    """
    def __init__(self):
        pass

    def get_fr_data(self, comp_code, period):
        """ 종목코드 입력 시 roe, roa, per, pbr 값을 가져와 return 한다.
        return 값의 period 는 
        @param comp_com : str
        @return : dict
        """

        return {"comp_code":comp_code, "period":period, "roe":0, "roa":0, "per":0, "pbr":0}

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()