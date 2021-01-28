import pymongo
import datetime

from finance import yahoo, analyses, financial_interactions

#Global Vars
mc = pymongo.MongoClient("mongodb://localhost:27017/")
yh = yahoo.YahooInteractions()
fi = financial_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")

#DBs
dgdb = mc['day_gainers']
dldb = mc['day_losers']

day_gainers = yh.get_day_gainers()
day_losers = yh.get_day_losers()

for stock in day_gainers:
    stock_collection = dgdb[stock[0] + '-' + str(datetime.datetime.now())]