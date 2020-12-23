import pymongo
import robin_stocks
import sys
import uuid

from . import financial_interactions

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#databases
market_data = mongo_client['market_data']

robinhood_interactions = financial_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")

#Utility function to parse data
def parse_historical_data(tickers, historical_data):
    for row in historical_data:
        print(row)


class GenerateData():
    def PopulateCollections(self, data_type, params):
        print("Retrieving " + data_type + " data...")
        
        if(data_type == "stock"):
            historical_data = robinhood_interactions.get_stock_historicals(params)

        print("Retrieved " + data_type + " data...")
        print("Writing to database...")

        parsed_historical_data = parse_historical_data(params[0], historical_data)