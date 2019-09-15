import datetime

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(
        request,
        'stock/index.html',
        {
            'title':'주식종목 추천',
            'year':datetime.datetime.now().year,
        }
    )