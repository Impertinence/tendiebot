import pymongo
import robin_stocks
import sys
import uuid

from . import financial_interactions, analyses

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#databases
market_data = mongo_client['market_data']

robinhood_interactions = financial_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")

class GenerateData():
    def PopulateCollections(self, data_type, params):
        print("Retrieving " + data_type + " data...")
        
        if(data_type == "stock"):
            historical_data = robinhood_interactions.get_stock_historicals(params)

        print("Retrieved " + data_type + " data...")
        print("Writing to database...")

        for row in historical_data:
            collection = market_data['asset-' + row.get('symbol')]
            collection.insert_one(row)
        
        print("Finished writing to database!")

    def PopulateAnalyses(self, ticker)
        