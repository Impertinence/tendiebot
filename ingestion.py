import pymongo
import threading
import time
import json
import sheets

from datetime import time as d_time
from datetime import datetime

from finance import market_interactions, analyses, financial_interactions

#Global Vars
mc = pymongo.MongoClient("mongodb://localhost:27017/")
yh = market_interactions.YAHOO()
fn = market_interactions.FINNHUB()
fi = financial_interactions.ROBINHOOD("pranavhegde11@gmail.com", "ae0iuwRmna1851")

#Times
pm_opening = d_time(9, 0, 0)
om_opening = d_time(9, 30, 0)
am_opening = d_time(4, 0, 0)
am_closing = d_time(6, 0, 0)

#Custom tickers from google sheets
SPREADSHEET_ID = "1wnXwk3pjunqLTbZ-ImL0GfjbXBQXWGrOPm12Zw5A-ZI"
SPREADSHEET_NAME = "stonks"

sa = sheets.SHEETS(SPREADSHEET_ID, SPREADSHEET_NAME)

#DBs
dgdb = mc['day_gainers']
dldb = mc['day_losers']
pdb = mc['positions']
sidb = mc['stock_info']

#Global Collections
interested_positions = pdb['interested']
invested_positions = pdb['invested']

day_gainers = yh.get_day_gainers()
day_losers = yh.get_day_losers()

print("[INGESTING]")

#Daily Gainers
def populateDayGainers():
    tickers = [stock[0] for stock in day_gainers]
    print("\n")
    print("[DAY_GAINERS]: " + str(datetime.datetime.now().date()))
    print("\n")

    for stock in day_gainers:
        ticker = stock[0]
        time = str(datetime.datetime.now())
        stock_collection = dgdb[time + '-' + ticker]

        stock_historicals = fi.get_stock_historicals([
            ticker,
            'hour',
            'week',
            'regular'
        ])

        if(stock_historicals != [None]):
            stock_collection.insert_many(stock_historicals)
            print('[DAY_GAINER_INSERTED]: ' + ticker)
        else:
            print('[DAY_GAINERS_ERR]: ' + ticker + " not available")

#Daily losers
def populateDayLosers():
    tickers = [stock[0] for stock in day_losers]

    print("\n")
    print("[DAY_LOSERS]: " + str(datetime.datetime.now()))
    print("\n")

    for stock in day_gainers:
        ticker = stock[0]
        time = str(datetime.datetime.now())
        stock_collection = dldb[time + '-' + ticker]

        stock_historicals = fi.get_stock_historicals([
            ticker,
            'hour',
            'week',
            'regular'
        ])

        if(stock_historicals != [None]):
            stock_collection.insert_many(stock_historicals)
            print('[DAY_LOSERS_INSERTED]: ' + ticker)
        else:
            print('[DAY_LOSERS_ERR]: ' + ticker + " not available")

def ingestWatchlist():
    watchlist = sa.getSheetsContent()

    for ticker in watchlist:
        price_info = fn.realtime_quote(ticker)
        stock_collection = interested_positions[ticker]

        if(datetime.now().time() >= am_opening):
            m_hours = "a"
        elif(datetime.now.time() >= om_opening):
            m_hours = "r"
        elif(datetime.now.time() >= pm_opening):
            m_hours = "p"
        
        inserted_price_info = {
            "time": str(datetime.now()),
            "market": m_hours,
            "c": price_info['c'],
            "o": price_info['o'],
            "l": price_info['l'],
            "h": price_info['h']
        }
        stock_collection.insert_one(inserted_price_info)

    time.sleep(60)

#Run all daily tasks
def DailyTasks():
    now = datetime.now().time()

    #Populate the daily movers collections
    if now == am_opening:
        populateDayLosers()
        populateDayGainers()

def ConstantTasks():
    ingestWatchlist()

while True:
    DailyTasks()
    ConstantTasks()