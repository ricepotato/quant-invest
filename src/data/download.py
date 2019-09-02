#-*- coding: utf-8 -*-
import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.append(base_path)

from common.logger import LogCfg
from common.database import Database
from common.database.dao import *
from crawler.downloader import CompGuideDownloader

log = logging.getLogger("qi.data.download")
log.setLevel(logging.DEBUG)

def start_download():
    db = Database()
    comp_dao = CompanyDao(db)
    comp_data_list = comp_dao.select()
    code_list = list(map(lambda comp : comp.code, comp_data_list))
    log.info("code_list len=%d", len(code_list))

    downloader = CompGuideDownloader()
    downloader.start_download(code_list)  

def main():
    log.info("download main.")
    start_download()

if __name__ == "__main__":
    main()