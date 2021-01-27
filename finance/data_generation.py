import pymongo
import robin_stocks
import sys
import uuid

from . import financial_interactions, analyses

#databases
market_data = mongo_client['market_data']

robinhood_interactions = financial_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")

class GenerateData():
    def GetCryptoHistoricals(self, params):
        data = robinhood_interactions.get_crypto_historicals(params)
        return data