def test_mongodb_repository_can_get_stock(mongo_repo):
    stock = mongo_repo.get("060310")
    assert stock


def test_mongodb_repository_can_get_all_stock_by_market(mongo_repo):
    kosdaq_stocks = mongo_repo.get_all("KOSDAQ")
    assert kosdaq_stocks
