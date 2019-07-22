# server
stock 정보를 저장하고있는 database Data 를 제공하는 REST API Server


# API 명세

method : GET

## /stock/{market_name}

ex)

/stock/KOSDAQ

/stock/KOSPI

## parameters

min_roa : 최소 ROA

min_per : 최소 PER

min_market_cap = 최소 시가총액

per_page = 종목 수


결과값

ex)
{
    "market":"KOSDAQ",
    "data":[
        {"num":1, "company_name":"네이버", "roa":15.3, "per":0.5, "roe":3.5, "pbr":6.7, "evebita":13.2, "eval_stock_price":98000, "stock_price":90000},
        {"num":1, "company_name":"카카오", "roa":15.3, "per":0.5, "roe":3.5, "pbr":6.7, "evebita":13.2, "eval_stock_price":98000, "stock_price":90000},
        {"num":1, "company_name":"안랩", "roa":15.3, "per":0.5, "roe":3.5, "pbr":6.7, "evebita":13.2, "eval_stock_price":98000, "stock_price":90000},
    ]
}



