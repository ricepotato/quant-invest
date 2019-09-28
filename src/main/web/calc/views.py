#-*- coding: utf-8 -*-
import datetime
import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

log = logging.getLogger("qi.web." + __name__)

def index(request):
    log.info("calc.views.index")
    log.info(request)
    #return JsonResponse({"msg":"hello world"})
    return render(request, "calc/index.html",
                 {
                     'title':'기간수익률 계산기',
                     'year':datetime.datetime.now().year,
                 })