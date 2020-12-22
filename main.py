#Written by Pranav Hegde
import pymongo

from finance import market_interactions
from storage import db_interactions

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Interactions
robinhood = market_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851",)

print(robinhood)
