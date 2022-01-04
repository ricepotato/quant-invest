def test_mongodb_repository_can_get_stock(mongo_repo):
    stock = mongo_repo.get("060310")
    assert stock
