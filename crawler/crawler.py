#-*- coding: utf-8 -*-

import os
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

from common.logger import LogCfg

log = logging.getLogger("qi.crawler.crawler")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

class Crawler(object):
    def __init__(self):
        pass

    def start(self):
        log.info("crawler start.")

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()