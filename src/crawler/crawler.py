#-*- coding: utf-8 -*-

import os
import sys
import logging
from bs4 import BeautifulSoup as BS
import requests

from .reader import CompFileReader

log = logging.getLogger("qi.crawler.crawler")

class CompGuideCrawler(object):
    """ company guide crawler 
    company guide site text parsing
    """
    def __init__(self):
        self.text = None
        self.reader = CompFileReader()

    def _get_text_by_id(self, comp_id):
        text = self.reader.read_text(comp_id)
        return text
    
    def _get_text_from_selector(self, bs, selector):
        log.debug("getting text from selector. sel=%s", selector)
        obj = bs.select(selector)
        return obj[0].text.strip().replace(",", "")

    def _parse_page(self, text):
        bs = BS(text, "html.parser")        
        #sel_period = "#highlight_D_A > table > thead > tr.td_gapcolor2 > th:nth-child(1)" <- 첫번째 period
        #roa = "#highlight_D_A > table > tbody > tr:nth-child(16) > td:nth-child(2)" <- 첫번째 period 의 roa
        #roe = "#highlight_D_A > table > tbody > tr:nth-child(17) > td:nth-child(2)" <- 첫번째 period 의 roa
        #per = "#highlight_D_A > table > tbody > tr:nth-child(21) > td:nth-child(2)"
        #pbr = "#highlight_D_A > table > tbody > tr:nth-child(22) > td:nth-child(2)"

        res = {}
        res["period"] = {}
        sel_mrk = "#svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)"
        #svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)
        #svdMainGrid1 > table > tbody > tr:nth-child(5) > td:nth-child(2)
        market_cap = self._get_text_from_selector(bs, sel_mrk)
        res["market_cap"] = int(market_cap)
        for idx in range(1, 6):
            sel_period = f"#highlight_D_Y > table > thead > tr.td_gapcolor2 > th:nth-child({idx})"
            sel_roa = f"#highlight_D_Y > table > tbody > tr:nth-child(16) > td:nth-child({idx+1})"
            sel_roe = f"#highlight_D_Y > table > tbody > tr:nth-child(17) > td:nth-child({idx+1})"
            sel_per = f"#highlight_D_Y > table > tbody > tr:nth-child(22) > td:nth-child({idx+1})"
            sel_pbr = f"#highlight_D_Y > table > tbody > tr:nth-child(22) > td:nth-child({idx+1})"
            
            period = self._get_text_from_selector(bs, sel_period)
            roa = self._str_to_float(self._get_text_from_selector(bs, sel_roa))
            roe = self._str_to_float(self._get_text_from_selector(bs, sel_roe))
            per = self._str_to_float(self._get_text_from_selector(bs, sel_per))
            pbr = self._str_to_float(self._get_text_from_selector(bs, sel_pbr))
            period = period.replace("/", "-")
            res["period"][period] = {"roa":roa, "roe":roe, "per":per, "pbr":pbr}
            log.debug("getting data. period=%s, data=%s", period, res["period"][period])
        
        return res

    def get_fr_data(self, comp_code):
        """ 종목코드 입력 시 roe, roa, per, pbr 값을 가져와 return 한다.
        return 값의 period 는 
        @param comp_com : str
        @return : dict
        """

        log.info("getting fr data comp_code=%s", comp_code)
        text = self._get_text_by_id(comp_code)
        res = self._parse_page(text)
        return res

    def _str_to_float(self, src):
        if src == "" or src == "N/A":
            return None

        try:
            return float(src)
        except ValueError as e:
            log.warning("type error. %s", e)
            return None

