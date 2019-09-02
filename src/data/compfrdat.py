#-*- coding: utf-8 -*-
import logging

from abc import ABCMeta, abstractmethod

log = logging.getLogger("qi.data.compfrdat")

class CompanyFrData(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self, comp_code, period):
        pass

class CompanyGuideFrData(CompanyFrData):
    """ company guide site 에서 crawling 해서 
    financial report 를 가져온다. """

    def __init__(self, crawler):
        self.crawler = crawler
        self.data = {}

    def get_data(self, comp_code):
        if self.data.get(comp_code, None) is None:
            fr_data = self.crawler.get_fr_data(comp_code)
            self.data[comp_code] = fr_data

        return self.data[comp_code]