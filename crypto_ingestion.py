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

#Time
now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

#Historical entries (Minute granularity)
btc_entries = []
eth_entries = []

#Live Entries (0.5 second granularity)
btc_live = []
eth_live = []

#Initial Ingestion of last 35 hours of data

#Bitcoin
for x in range(0, 7):
    entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)
    btc_entries.extend(entries)
    previous -= intervals
    now -= intervals
    time.sleep(1)

#Ethereum
for x in range(0, 7):
    entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
    eth_entries.extend(entries)
    previous -= intervals
    now -= intervals
    time.sleep(1)

#Live Ingestion
while True:
    new_eth_entry = public_client.get_product_ticker("ETH-USD")
    new_btc_entry = public_client.get_product_ticker("BTC-USD")

    btc_live.append(new_btc_entry)
    eth_live.append(new_eth_entry)

    btc_analyses = analyses.Analyses(btc_live)
    eth_analyses = analyses.Analyses(eth_live)
btc_analyses.stochastics("bid", "ask", "price", 14, 3)

    time.sleep(0.5)

#Historical ingestion
while True:
    new_eth_entries = public_client.get_product_ticker("ETH-USD")
    new_btc_entries = public_client.get_product_ticker("BTC-USD")

    time.sleep(60)