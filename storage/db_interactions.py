import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

class StockDB():
    def insert_stock(info):
        print(info)