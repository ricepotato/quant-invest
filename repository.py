from abc import abstractmethod
import os
import pymongo
from pymongo.mongo_client import MongoClient

from models import Stock


class Repository:
    @abstractmethod
    def add(self, stock: Stock) -> bool:
        pass

    @abstractmethod
    def get(self, code: str) -> Stock:
        pass


class MongodbRepository(Repository):
    def add(self, stock: Stock) -> bool:
        self.client = self._get_client()
        sc = self.client.qi.stock
        obj = sc.find_one({"code": stock.code})
        if obj is None:
            sc.insert_one(stock.to_dict())

        return True

    def get(self, code: str) -> Stock:
        self.client = self._get_client()
        sc = self.client.qi.stock
        obj = sc.find_one({"code": code})
        return Stock.from_dict(obj)

    def _get_mongo_client(self, host, user, password) -> MongoClient:
        """mongodb+srv://ricepotato:<password>@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit"""
        connection_string = f"mongodb+srv://{user}:{password}@{host}"
        client = pymongo.MongoClient(
            connection_string, ssl=True, tlsAllowInvalidCertificates=True
        )
        return client

    def _get_client(self) -> MongoClient:
        host = os.environ.get("MONGODB_HOST")
        user = os.environ.get("MONGODB_USER")
        password = os.environ.get("MONGODB_PASSWORD")
        client = self._get_mongo_client(host, user, password)
        return client
