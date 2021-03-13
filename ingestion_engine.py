import pymongo
import threading
import time
import json
import sheets
import csv

from datetime import time as d_time
from datetime import datetime

from finance import interactions, analyses

#Global Vars
mc = pymongo.MongoClient("mongodb://localhost:27017/")

yh = interactions.YAHOO()
fn = interactions.FINNHUB()
oi = interactions.OPENINSIDER()
mw = interactions.MARKETWATCH()
fi = interactions.ROBINHOOD("pranavhegde11@gmail.com", "ae0iuwRmna1851")

#Small Cap tickers
smallcap = []
with open('files/all_smallcap.csv', newline="") as smallcap_file:
    tickers = csv.reader(smallcap_file, delimiter=',', quotechar='"')
    for t in tickers:
        smallcap = t

#Medium Cap tickers

#Custom tickers from google sheets
SPREADSHEET_ID = "1wnXwk3pjunqLTbZ-ImL0GfjbXBQXWGrOPm12Zw5A-ZI"
SPREADSHEET_NAME = "stonks"

#Times
pm_opening = d_time(9, 0, 0)
om_opening = d_time(9, 30, 0)
am_opening = d_time(4, 0, 0)
am_closing = d_time(6, 0, 0)

sa = sheets.SHEETS(SPREADSHEET_ID, SPREADSHEET_NAME)

#DBs
dgdb = mc['day_gainers']
dldb = mc['day_losers']
pdb = mc['positions']
sidb = mc['stock_info']

#Organization by Capital
smallcap_db = mc['smallcap']
mediumcap_db = mc['mediumcap']

#Global Collections
interested_positions = pdb['interested']
invested_positions = pdb['invested']

day_gainers = yh.get_day_gainers()
day_losers = yh.get_day_losers()

#start ingestion engine
def start():
	constant_tasks()
	daily_tasks()

#Daily Gainers
def day_winners():
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
def day_losers():
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

#Ingest the watchlist
def watchlist():
    watchlist = sa.getSheetsContent()

    for ticker in watchlist:
        price_info = fn.realtime_quote(ticker)
        stock_collection = interested_positions[ticker]

        if(datetime.now().time() >= am_opening):
            m_hours = "a"
        elif(datetime.now().time() >= om_opening):
            m_hours = "r"
        elif(datetime.now().time() >= pm_opening):
            m_hours = "p"
        
        inserted_price_info = {
            "t": str(datetime.now()),
            "m": m_hours,
            "c": price_info['c'],
            "o": price_info['o'],
            "l": price_info['l'],
            "h": price_info['h']
        }

        stock_collection.insert_one(inserted_price_info)

    time.sleep(60)

#Ingest smallcaps
def get_smallcap():
    first_batch = smallcap[:2000]
    second_batch = smallcap[2000:4000]
    third_batch = smallcap[4000:4300]

    #Ingest first batch of smallcap tickers
    for ticker in first_batch:
        stock_collection = smallcap_db[ticker]  

    for ticker in second_batch:
        stock_collection = smallcap_db[ticker]

    for ticker in third_batch:
        stock_collection = smallcap_db[ticker]

    print("[INGESTED SMALLCAP]")
    time.sleep(3600)

#Populate crypto db
def populate_crypto():
    
    time.sleep(60)

#Run all daily tasks
def daily_tasks():
    now = datetime.now().time()

    #Populate the daily movers collections
    if now == am_opening:
        day_losers()
        day_winners()

def constant_tasks():
    while True:
        populate_crypto()

if __name__ == '__main__':
	start()
