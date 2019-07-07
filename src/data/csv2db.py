#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

cur_path = os.path.dirname(__file__)
comm_path = os.path.abspath(os.path.join(cur_path, "..", "common"))

sys.path.append(comm_path)

import logger.logcfg
from database.dao import *
from stockreder import SCReader

log = logging.getLogger("qi.data.csv2db")

def main():

    kosdaq = os.path.join(cur_path, "KOSDAQ.csv")
    kospi = os.path.join(cur_path, "KOSPI.csv")

    reader = SCReader()
    kosdaq_data = reader.read_file(kosdaq)
    





if __name__ == "__main__":
    main()