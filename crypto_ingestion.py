import coinbasepro as cbp

import numpy as np
import pandas as pd

import datetime
import time
import pymongo

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


#Live Ingestion
while True:
    #Retrieve half-second entries
    new_eth_entry = public_client.get_product_ticker("ETH-USD")
    new_btc_entry = public_client.get_product_ticker("BTC-USD")

    #Append half-second entries
    btc_live.append(new_btc_entry)
    eth_live.append(new_eth_entry)

    #Analyses object
    btc_analyses = analyses.Analyses(btc_live)
    eth_analyses = analyses.Analyses(eth_live)

    #Half-second pause before restarting loop
    time.sleep(0.5)

#Starting time for historical ingestion
now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

#Historical ingestion
while True:
    new_eth_entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
    new_btc_entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

    #Publish to mongo database

    previous -= intervals
    now -= intervals

    time.sleep(60)
