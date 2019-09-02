import os
import logging

log = logging.getLogger("qi.crawler.reader")

cur_path = os.path.dirname(__file__)

class FileReader:
    def __init__(self):
        self.data_path = os.path.join(cur_path, "comp_guide_html")

    def read_text(self, comp_id):
        txt_path = os.path.join(self.data_path, str(comp_id))
        with open(txt_path, "r") as f:
            text = f.read()
        return text
