#-*- coding: utf-8 -*-
import logging

from abc import ABCMeta, abstractmethod

log = logging.getLogger("qi.data.compfrdat")

class CompanyFrData(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self, comp_code):
        pass

class CompanyGuideFrData(CompanyFrData):
    """ company guide site 에서 crawling 해서 
    financial report 를 가져온다. """

    def __init__(self, crawler):
        self.crawler = crawler
        self.json_reader = None
        self.data = {}

    def get_data(self, comp_code):
        fr_data = self._get_from_json(comp_code)
        if fr_data:
            return fr_data
            
        if self.data.get(comp_code, None) is None:
            fr_data = self.crawler.get_fr_data(comp_code)
            self.data[comp_code] = fr_data

        return self.data[comp_code]

    def _get_from_json(self, comp_code):
        fr_data = self.json_reader.read_json(comp_code)
        return fr_data
