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

def add_comp_guide_link(comp_code):
    return f"<a target='_blank' href='http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?gicode=A{comp_code}&MenuYn=Y'>{comp_code}</a>"

def row_func(item):
    return [item["total_rank"], f"{item['company_name']}(" + add_comp_guide_link(item['code']) + ")", 
            f"{item['roa']}({item['roa_rank']})", 
            f"{item['per']}({item['per_rank']})", 
            item["roe"], item["pbr"], "", item["market_cap"]]

def args_parse(request):
    market = request.GET['market']
    year = request.GET["year"]
    length = request.GET.get("length", 10)
    draw = request.GET.get("draw")
    min_mrkcap = request.GET.get("min_mrkcap", None)
    length = int(length)
    if min_mrkcap is None or min_mrkcap == "":
        min_mrkcap = None
    else:
        min_mrkcap = int(min_mrkcap)
    draw = int(draw)

    return {"market":market, "year":year, 
            "length":length, "draw":draw, 
            "min_mrkcap":min_mrkcap}

def api_stock(request):
    qi_api = QIApi()
    args = args_parse(request)
    
    stock_data = qi_api.get_stock(args["market"], args["year"], 
                                  args["min_mrkcap"])
    stock_list = stock_data["stock_list"]
    stock_list = stock_list[:args["length"]]
    table_data = list(map(row_func, stock_list))
    data = {
        "draw":args["draw"],
        "recordsTotal":len(stock_data),
        "recordsFiltered":len(stock_data),
        "data": table_data
    }
    return JsonResponse(data)