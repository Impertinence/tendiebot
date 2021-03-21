import coinbasepro as cbp

import matplotlib.pyplot as plt
import numpy as np

import datetime
import time
import pymongo

now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

public_client = cbp.PublicClient()

btc_entries = []
eth_entries = []

for x in range(0, 7):
    entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)
    btc_entries.extend(entries)
    previous -= intervals
    now -= intervals
    time.sleep(1)

for x in range(0, 7):
    entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
    eth_entries.extend(entries)
    previous -= intervals
    now -= intervals
    time.sleep(1)

btc_close = [entry['close'] for entry in btc_entries]
btc_time = [entry['time'] for entry in btc_entries]

eth_close = [entry['close'] for entry in eth_entries]
eth_time = [entry['time'] for entry in eth_entries]

plt.plot(eth_time, eth_close)
plt.show()