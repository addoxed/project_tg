from pymongo import MongoClient
from config import settings

class Database:
    def __init__(self, name_db: str):
        self.client = MongoClient(settings.DB_URL)
        self.db = self.client[settings.DB_CLUSTER]
        self.collection = self.db[name_db]
    
    def insert_one(self, _data: dict):
        return self.collection.insert_one(_data)

    def find_one(self, _query: dict):
        return self.collection.find_one(_query)

    def find_all(self, _query: dict | None = None):
        return self.collection.find(_query)

    def update_one(self, _query: dict, _update: dict):
        return self.collection.update_one(_query, {"$set": _update})

    def delete_one(self, _query: dict):
        return self.collection.delete_one(_query)
    