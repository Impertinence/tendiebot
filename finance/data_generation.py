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
    def PopulateCryptoHistorical(self, params):
        data = robinhood_interactions.get_crypto_historicals(params)
        return data