#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

log = logging.getLogger('qi.server.app')

from server import APIServer
from resources.stock import Stock

def main():
    server = APIServer()
    server.add_resource(Stock, "/stock")
    server.run(port=8091)

if __name__ == "__main__":
    main()