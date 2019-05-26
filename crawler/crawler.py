#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))
#comm_path = os.path.abspath(os.path.join(cur_path, "..", "common"))

sys.path.append(base_path)

from common.logger.logger import LogCfg

log = logging.getLogger("qi.crawler.crawler")

class Crawler(object):
    def __init__(self):
        pass

    def start(self):
        log.info("crawler start.")

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()