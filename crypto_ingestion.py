import coinbasepro as cbp

import numpy as np
import pandas as pd

import datetime
import time
import pymongo
import _thread

from finance import analyses
from misc import plotting

#APIs
public_client = cbp.PublicClient()
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#Relevant Databases and Collections
crypto_db = mongo_client['crypto']

btc_live = crypto_db['btc_live']
eth_live = crypto_db['eth_live']
btc_historical = crypto_db['btc_historical']
eth_historical = crypto_db['eth_historical']

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
    while True:
        #Retrieve half-second entries
        new_eth_entry = public_client.get_product_ticker("ETH-USD")
        new_btc_entry = public_client.get_product_ticker("BTC-USD")

        #Append half-second entries
        btc_live.insert_one(new_btc_entry)
        eth_live.insert_one(new_eth_entry)

        #Analyses object
        btc_analyses = analyses.Analyses(btc_live)
        eth_analyses = analyses.Analyses(eth_live)

        #Half-second pause before restarting loop
        time.sleep(0.5)

#Historical ingestion
def historical_ingestion(thread_name, test):
    now = datetime.datetime.now() + datetime.timedelta(hours=4)
    intervals = datetime.timedelta(minutes=300)
    previous = now - intervals

    # #Historical ingestion
    while True:
        print("test")
        new_eth_entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
        new_btc_entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

        #Publish to mongo database
        eth_historical.insert_many(new_eth_entries)
        btc_historical.insert_many(new_btc_entries)

        previous -= intervals
        now -= intervals

        time.sleep(60)