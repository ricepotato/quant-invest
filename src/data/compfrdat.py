#-*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class CompanyFrData(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self, comp_code, period):
        pass

class CompanyGuideFrData(CompanyFrData):
    """ company guide site 에서 crawling 해서 
    financial report 를 가져온다. """

    def __init__(self, crawler):
        self.crawler = crawler

    def get_data(self, comp_code, period):
        data = self.crawler.get_data(comp_code, period)
        # {"comp_code":comp_code, "period":"2018/12", "roe":0, "roa":0, "per":0, "pbr":0}
        return data