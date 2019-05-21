#-*- coding: utf-8 -*-

import logging

log = logging.getLogger("qi.crawler.crawler")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()