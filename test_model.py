from models import Stock, FinancialReport


def test_stock_model():
    stock = Stock("005930", "삼성전자", "KOSPI", market_cap=5279790)
    assert stock


def test_sotck_model_from_dict():
    stock_dict = {
        "code": "054620",
        "name": "APS홀딩스",
        "category_code": "116409",
        "desc": "기타 금융업",
        "market": "KOSDAQ",
        "market_cap": 1587,
        "fr": {"2016-03": {"per": 1, "pbr": 2, "roa": 3, "roe": 4}},
    }
    stock = Stock.from_dict(stock_dict)
    assert stock.code == stock_dict["code"]
    assert stock.name == stock_dict["name"]
    assert stock.fr
    assert stock.fr["2016-03"].period == "2016-03"
    assert stock.fr["2016-03"].code == stock.code
    assert stock.fr["2016-03"].per == 1


def test_fr_equal():
    fr1 = FinancialReport("code1", "2015-03", 1, 2, 3, 4)
    fr2 = FinancialReport("code1", "2015-03", 2, 3, 4, 5)
    assert fr1 == fr2

    some_list = [fr1]
    assert fr2 in some_list
