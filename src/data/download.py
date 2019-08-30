#-*- coding: utf-8 -*-
import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.append(base_path)

from common.logger import LogCfg
#from common.database.database import Database
from common.database.dao import *
from crawler.downloader import CompGuideDownloader

log = logging.getLogger("qi.data.download")

def start_download():
    comp_dao = CompanyDao()
    comp_data_list = comp_dao.select()
    code_list = list(map(lambda comp : comp.code, comp_data_list))
    log.info("code_list len=%d", len(code_list))

def main():
    log.info("download main.")
    start_download()

if __name__ == "__main__":
    main()