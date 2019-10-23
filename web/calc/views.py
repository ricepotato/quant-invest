#-*- coding: utf-8 -*-
import datetime
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from api import QIApi

log = logging.getLogger("qi.web." + __name__)

def index(request):
    return render(request, "calc/index.html",
                 {
                     'title':'기간수익률 계산기',
                     'year':datetime.datetime.now().year,
                 })

def calc_list(request):
    qi_api = QIApi()
    res = {"res":qi_api.get_er()}
    return render(request, "calc/list.html", res)

class CalcAPI:
    def __init__(self, request):
        self.api = QIApi()
        self.request = request

    def get(self):
        res = {"res":self.api.get_er()}
        return JsonResponse(res)

    def post(self):
        code = self.request.POST["comp_code"]
        st_date = self.request.POST["st_date"]
        hold = int(self.request.POST["hold"])
        period = int(self.request.POST["period"])
        res = self.api.post_er(code, st_date, hold, period)
        return JsonResponse(res)

    def delete(self, id):
        #id = self.request.GET["id"]
        res = self.api.delete_er(id)
        return JsonResponse(res)

@csrf_exempt
def api_calc(request):
    api = CalcAPI(request)
    method_map = {
        "POST":api.post,
        "GET":api.get,
        "DELETE":api.delete
    }
    return method_map[request.method]()

def calc_delete(request, id):
    log.info("calc_delete %s", str(id))
    api = CalcAPI(request)
    return api.delete(id)