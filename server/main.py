#-*- coding: utf-8 -*-
import os
import sys
import logging

import qi.logger.logcfg
from app import server

log = logging.getLogger("qi")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
log = logging.getLogger("qi.server.main")

def main():
    server.run(port=8089)

if __name__ == "__main__":
    main()
