#-*- coding: utf-8 -*-
import os
import json
import logging

log = logging.getLogger("qi.crawler.reader")

cur_path = os.path.dirname(__file__)

class CompFileReader:
    def __init__(self):
        self.data_path = os.path.join(cur_path, "comp_guide_html")

    def read_text(self, comp_code):
        txt_path = os.path.join(self.data_path, f"{comp_code}.html")
        with open(txt_path, "r") as f:
            text = f.read()
        return text

class CompJsonReader:
    def __init__(self):
        self.data_path = os.path.join(cur_path, "comp_guide_json")
    
    def read_json(self, comp_code):
        json_path = os.path.join(self.data_path, f"{comp_code}.json")
        try:
            with open(json_path, "r") as f:
                text = f.read()
        except IOError as e:
            log.warning("json reader io error. comp_code=%s, %s",comp_code, e)
            return None
        return json.loads(text)
