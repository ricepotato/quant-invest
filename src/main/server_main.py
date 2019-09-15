#-*- coding: utf-8 -*-
import os
import sys
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.join(cur_path, "server")
sys.path.append(base_path)

from server.app import server

log = logging.getLogger("qi")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
log = logging.getLogger("qi.server.main")

def main():
    server.run()

if __name__ == "__main__":
    main()
