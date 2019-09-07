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
        with open(txt_path, "rb") as f:
            data = f.read()
        text = self._try_decode(data)
        return text

    def _try_decode(self, data):
        encodings = ["utf-8", "ascii", "ansi", "utf-16"]
        for encoding in encodings:
            try:
                text = data.decode(encoding)
                return text
            except UnicodeDecodeError as e:
                log.warning("decode error. %s", e)
        raise UnicodeDecodeError("file reader decode error.")

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
