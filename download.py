#-*- coding: utf-8 -*-
import os
import sys
import logging

import qi.logger.logcfg
from qi.database import Database
from qi.database.dao import *
from qi.utils.downloader import CompGuideDownloader

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