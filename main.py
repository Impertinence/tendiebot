#Written by Pranav Hegde
import pymongo

from finance import market_interactions

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Interactions
robinhood = market_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851",)

#DB Interactions
stock_market = myclient["stock_market"]
crypto_market = myclient["crypto_market"]
miscellaneous = myclient["miscellaneous"]

print(robinhood)
