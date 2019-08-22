#-*- coding: utf-8 -*-

import os
import sys
import logging
from bs4 import BeautifulSoup as BS
import requests

log = logging.getLogger("qi.crawler.crawler")

class CompGuideCrawler(object):
    """ company guide crawler 
    company guide site 에 방문하여 financial report data 를 가져온다.
    """
    def __init__(self):
        self.url = url = "http://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode=A{}"
        self.text = None
    
    def _get_text_from_url(self, url):
        log.debug("getting text from url. url=%s", url)
        r = requests.get(url)
        self.text = r.text
        return r.text

    def _get_url(self, gicode):
        url = self.url.format(gicode)
        return url
    
    def _get_text_from_selector(self, bs, selector):
        log.debug("getting text from selector. sel=%s", selector)
        obj = bs.select(selector)
        return obj[0].text.strip()

    def _parse_page(self, text):
        bs = BS(text, "html.parser")        
        #sel_period = "#highlight_D_A > table > thead > tr.td_gapcolor2 > th:nth-child(1)" <- 첫번째 period
        #roa = "#highlight_D_A > table > tbody > tr:nth-child(16) > td:nth-child(2)" <- 첫번째 period 의 roa
        #roe = "#highlight_D_A > table > tbody > tr:nth-child(17) > td:nth-child(2)" <- 첫번째 period 의 roa
        #per = "#highlight_D_A > table > tbody > tr:nth-child(21) > td:nth-child(2)"
        #pbr = "#highlight_D_A > table > tbody > tr:nth-child(22) > td:nth-child(2)"

        res = {}
        for idx in range(1, 4):
            sel_period = f"#highlight_D_A > table > thead > tr.td_gapcolor2 > th:nth-child({idx})"
            sel_roa = f"#highlight_D_A > table > tbody > tr:nth-child(16) > td:nth-child({idx+1})"
            sel_roe = f"#highlight_D_A > table > tbody > tr:nth-child(17) > td:nth-child({idx+1})"
            sel_per = f"#highlight_D_A > table > tbody > tr:nth-child(21) > td:nth-child({idx+1})"
            sel_pbr = f"#highlight_D_A > table > tbody > tr:nth-child(22) > td:nth-child({idx+1})"
            
            period = self._get_text_from_selector(bs, sel_period)
            roa = self._get_text_from_selector(bs, sel_roa)
            roe = self._get_text_from_selector(bs, sel_roe)
            per = self._get_text_from_selector(bs, sel_per)
            pbr = self._get_text_from_selector(bs, sel_pbr)
            period = period.replace("/", "-")
            res[period] = {"roa":roa, "roe":roe, "per":per, "pbr":pbr}
            log.debug("getting data. period=%s, data=%s", period, res[period])
        
        return res

    def get_fr_data(self, comp_code, period):
        """ 종목코드 입력 시 roe, roa, per, pbr 값을 가져와 return 한다.
        return 값의 period 는 
        @param comp_com : str
        @return : dict
        """

        url = self._get_url(comp_code)
        text = self._get_text_from_url(url)
        res = self._parse_page(text)
        return res

def main():
    log.info("hello world")

if __name__ == "__main__":
    main()