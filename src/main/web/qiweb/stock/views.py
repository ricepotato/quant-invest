#-*- coding: utf-8 -*-
import json
import logging
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

"""def post_list3(request):
    return JsonResponse({
        'message' : '안녕 파이썬 장고',
        'items' : ['파이썬', '장고', 'AWS', 'Azure'],
    }, json_dumps_params = {'ensure_ascii': True})"""

from api import QIApi
# Create your views here.

log = logging.getLogger("qi.web" + __name__)

def index(request):
    return render(
        request,
        'stock/index.html',
        {
            'title':'주식종목 추천',
            'year':datetime.datetime.now().year,
        }
    )

def api_stock(request):
    qi_api = QIApi()
    market = request.GET['market']
    year = request.GET["year"]
    length = request.GET.get("length", 10)
    draw = request.GET.get("draw")
    length = int(length)
    stock_data = qi_api.get_stock(market, year)
    stock_list = stock_data["stock_list"]
    stock_list = stock_list[:length]
    log.info("length=%d", length)
    data_processed = map(lambda item: [item["total_rank"], item["company_name"], 
                                       item["roa"], item["per"], item["roe"], item["pbr"], "", ""], stock_list)
    data = {
        "draw":int(draw),
        "recordsTotal":len(stock_data),
        "recordsFiltered":len(stock_data),
        "data": list(data_processed)
    }
    #{"market": "KOSDAQ", "stock_list": [{"code": "032940", "company_name": "\uc6d0\uc775", "date_insert": "2019-09-05 20:22:43", 
    # "market_cap": null, "pbr": 0.58, "per": 0.58, "per_rank": 53, "period": "2016-12", "roa": 53.1, "roa_rank": 7, "roe": 99.91, 
    # "total_rank": 60}
    return JsonResponse(data)