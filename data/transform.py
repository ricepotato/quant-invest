#-*- coding: utf-8 -*-
import os
import json
import logging

log = logging.getLogger("qi.crawler.transform")

cur_path = os.path.dirname(__file__)

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error("transform error. comp_code=%s, %s",args[1], e)
    return wrapper

class Transform:

    def __init__(self):
        self.html_path = os.path.join(cur_path, "comp_guide_html")
        self.json_path = os.path.join(cur_path, "comp_guide_json")
        self.crawler = None

    def rename(self):
        for filename in os.listdir(self.html_path):
            filepath = os.path.join(self.html_path, filename)
            to_filepath = os.path.join(self.html_path, f"{filename}.html")
            log.info(to_filepath)
            os.rename(filepath, to_filepath)

    @handle_exception
    def transfrom(self, comp_code):
        out_path = os.path.join(self.json_path, f"{comp_code}.json")
        if os.path.exists(out_path):
            log.debug("json file already exist. path=%s", out_path)
            return out_path
        res = self.crawler.get_fr_data(comp_code)
        text = json.dumps(res, indent=4)
        with open(out_path, "w") as f:
            f.write(text)
        return out_path



    
            
