
from app.database.mongo import get_client

class MongoDao(object):

    def __init__(self):
        self.client = get_client()
        self.coll = self.client.qi.stock


    def insert(self, obj):
        return self.coll.insert_one(obj)

    def find_by_code(self, code):
        obj = self.coll.find_one({"code": code})
        return obj

    def get_stock_list(self, market):
        rs = self.coll.find({"market": market})
        return list(rs)

