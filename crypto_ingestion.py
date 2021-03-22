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

btc_entries = []
eth_entries = []

btc_stochs = []
eth_stochs = []

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

# #Live Ingestion
# while True:
#     new_eth_entry = public_client.get_product_ticker("ETH-USD")
#     new_btc_entry = public_client.get_product_ticker("BTC-USD")

#     btc_entries.extend(new_btc_entry)
#     eth_entries.extend(new_eth_entry)

#     eth_analyses = analyses.Analyses(eth_entries)



#     time.sleep(60)

btc_analyses = analyses.Analyses(btc_entries)

stochastics_df = btc_analyses.stochastics("low", "high", "close", 14, 3)

plot = plotting.Plot(stochastics_df)

plot.stochastics()