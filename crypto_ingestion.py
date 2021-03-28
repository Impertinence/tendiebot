import cbpro as cbp

import numpy as np
import pandas as pd

import datetime
import time
import pymongo
import threading

from finance import analyses
from misc import plotting
from bson.decimal128 import Decimal128
from decimal import Decimal

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#Relevant Databases and Collections
crypto_db = mongo_client['crypto']

all_live = crypto_db['live']
btc_historical = crypto_db['btc_historical']
eth_historical = crypto_db['eth_historical']

#APIs
public_client = cbp.PublicClient()
websocket_client = cbp.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products=["BTC-USD", "ETH-USD"], channels=["ticker"], mongo_collection=all_live, should_print=False)

ingestion_ready = True

#Empty live collection before ingestion
all_live.delete_many({})

#Ingest time difference
def time_difference_ingestion(thread_name, test):
    #Ingest time difference
    if(len(eth_historical.find_one()) > 0 and len(btc_historical.find_one()) > 0):
        now = ((datetime.datetime.now() + datetime.timedelta(hours=4)) - datetime.datetime(1970, 1, 1)).total_seconds()
        interval = (datetime.timedelta(minutes=300)).total_seconds()

        #Get most recent entries and time
        last_eth_entry = eth_historical.find_one()
        last_btc_entry = btc_historical.find_one()

        last_btc_time = (last_btc_entry['time'] - datetime.datetime(1970, 1, 1)).total_seconds()
        last_eth_time = (last_eth_entry['time'] - datetime.datetime(1970, 1, 1)).total_seconds()

        #Get num of loops
        num_btc_loops = (now - last_btc_time) / interval
        num_eth_loops = (now - last_eth_time) / interval

        #BTC updates
        for x in range(0, num_btc_loops):
            time.sleep(1)

        #ETH updates
        for x in range(0, num_eth_loops):
            time.sleep(1)


#Live ingestion
def live_ingestion(thread_name, test):
    #Start live ingestion
    websocket_client.start()

#Historical ingestion
def historical_ingestion(thread_name, test):
    now = datetime.datetime.now() + datetime.timedelta(hours=4)
    intervals = datetime.timedelta(minutes=300)
    previous = now - intervals

    # # #Historical ingestion
    # while (ingestion_ready == True):
    #     new_eth_entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
    #     new_btc_entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

    #     #Publish to mongo database
    #     eth_historical.insert_many(new_eth_entries)
    #     btc_historical.insert_many(new_btc_entries)

    #     previous -= intervals
    #     now -= intervals

    #     time.sleep(60)

#Start all threads
if __name__ == "__main__":
    #Init threads1
    # time_diff_ingestion = threading.Thread(target=time_difference_ingestion, args=("time_diff", 1))
    live_ingestion = threading.Thread(target=live_ingestion, args=("live", 1))
    # historical_ingestion = threading.Thread(target=historical_ingestion, args=("historical", 1))

    #Start threads
    # time_diff_ingestion.start()
    live_ingestion.start()
    # historical_ingestion.start()