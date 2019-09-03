#-*- coding: utf-8 -*-

import os
import requests
import logging
import multiprocessing
from multiprocessing import Pool

log = logging.getLogger("qi.crawler.downloader")

class CompGuideDownloader:

    def __init__(self):
        self.base_url = "http://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode=A{}"
        self.path = self._downlad_path()
        self.processes = 5

    def _downlad_path(self):
        cur_path = os.path.dirname(__file__)
        download_path = os.path.join(cur_path, "comp_guide_html")
        return os.path.abspath(download_path)

    def start_download(self, comp_ids):
        log.info("start download...")
        #multiprocessing.set_start_method("spawn")
        with Pool(self.processes) as p:
            res = p.map(self._get_file_req, comp_ids)
        #res = list(map(lambda comp_id : self._get_file_req(comp_id), comp_ids))

        return res

    def _get_file_req(self, comp_id):
        log.debug("preparing file download.. comp_id=%s", comp_id)
        filepath = os.path.join(self.path, f"{comp_id}.html")
        url = self.base_url.format(comp_id)
        return self._download(url, filepath)
        
    def _download(self, url, filepath):
        if os.path.exists(filepath):
            log.debug("file already exist. skip.. %s", filepath)
            return filepath
        
        log.debug("request file... url=%s", url)
        res = requests.get(url)
        with open(filepath, "w") as f:
            f.write(res.text)
        log.debug("download complete. filepath=%s", filepath)
        return filepath
