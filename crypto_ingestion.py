import cbpro as cbp
import coinbasepro as cbp2

import numpy as np
import pandas as pd

import datetime
import time
import pymongo
import threading
import decimal

from finance import analyses
from misc import plotting
from bson.decimal128 import Decimal128

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

#Relevant Databases and Collections
crypto_db = mongo_client['crypto']

all_live = crypto_db['live']
btc_historical = crypto_db['btc_historical']
eth_historical = crypto_db['eth_historical']

btc_historical_training = crypto_db['btc_training_historical']
eth_historical_training = crypto_db['eth_training_historical']

#APIs
public_client = cbp2.PublicClient()
websocket_client = cbp.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products=["BTC-USD", "ETH-USD"], channels=["ticker"], mongo_collection=all_live, should_print=False)

ingestion_ready = True

#Empty live collection before ingestion
all_live.delete_many({})

#Ingest time difference
def time_difference_ingestion(thread_name, start_time):
	print("[TIME_DIFFERENCE_INGESTION] Started at " + str(start_time))

	#If historical collections not empty
	if(len(list(btc_historical.find())) > 0 and len(list(eth_historical.find())) > 0):
		recent_btc_historical = btc_historical.find()[0]
		recent_eth_historical = eth_historical.find()[0]

		now = datetime.datetime.now() + datetime.timedelta(hours=4)
		interval = datetime.timedelta(minutes=300)
		previous = now - interval

		#Calculate eth ingestion epochs
		odd_eth_epoch = int((now - recent_eth_historical['time']) / datetime.timedelta(minutes=1)) % 300
		num_eth_epochs = int(int((now - recent_eth_historical['time']) / datetime.timedelta(minutes=1)) / 300)

		#Calculate btc ingestion epochs
		odd_btc_epoch = int(((datetime.datetime.now() + datetime.timedelta(hours=4)) - recent_btc_historical['time']) / datetime.timedelta(minutes=1)) % 300
		num_btc_epoch = int(int(((datetime.datetime.now() + datetime.timedelta(hours=4)) - recent_btc_historical['time']) / datetime.timedelta(minutes=1)) / 300)

		#Retrieve odd epochs
		odd_eth_epoch_values = public_client.get_product_historic_rates("ETH-USD", now - datetime.timedelta(minutes=odd_eth_epoch), now)
		odd_btc_epoch_values = public_client.get_product_historic_rates("BTC-USD", now - datetime.timedelta(minutes=odd_btc_epoch), now)

		#BTC update loop
		for x in range(0, num_btc_epoch):
			btc_epoch_values = public_client.get_product_historic_rates("BTC-USD", now, previous, 60)



			now -= interval
			previous -= interval

			time.sleep(1)

		#ETH update loop
		for x in range(0, num_eth_epochs):
			eth_epoch_values = public_client.get_product_historic_rates("ETH-USD", now, previous, 60)

			now -= interval
			previous -= interval

			time.sleep(1)
	else:
		now = datetime.datetime.now() + datetime.timedelta(hours=4)
		intervals = datetime.timedelta(minutes=300)
		previous = now - intervals

		for x in range(0, 50):
			raw_eth_entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
			raw_btc_entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

			eth_entries = [{k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in i.items()} for i in raw_eth_entries]
			btc_entries = [{k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in i.items()} for i in raw_btc_entries]

			eth_historical.insert_many(eth_entries)
			btc_historical.insert_many(btc_entries)

			print("[TIME_DIFFERENCE_INGESTION]: ETH_EPOCH " + str(x) + " Completed!")
			print("[TIME_DIFFERENCE_INGESTION]: BTC_EPOCH " + str(x) + " Completed!")

			previous -= intervals
			now -= intervals

			time.sleep(0.5)

	ingestion_ready = True
	print("[TIME_DIFFERENCE_INGESTION]: Ended at " + str(datetime.datetime.now()))

#Live ingestion
def live_ingestion(thread_name, start_time):
    #Start live ingestion
    interval_start_time = start_time

    print("[LIVE_INGESTION]: Started at " + str(start_time))
    websocket_client.start()

    while True:
    	#Reset live every 2 hours
    	if((datetime.datetime.now() - start_time) % datetime.timedelta(hours=2) == 0):
    	    live_crypto.delete_many({})
    	    interval_start_time = datetime.datetime.now()

    	time.sleep(1)

#Historical ingestion
def historical_ingestion(thread_name, start_time):
    now = None
    intervals = None
    previous = None

    #If ready for historical ingestion init time vals
    while(ingestion_ready == True):
	    now = datetime.datetime.now() + datetime.timedelta(hours=4)
	    intervals = datetime.timedelta(minutes=300)
	    previous = now - intervals
	    break

    print("[HISTORICAL_INGESTION]: Started at " + str(start_time))

    #Historical ingestion
    while (ingestion_ready == True):
    	raw_eth_entries = public_client.get_product_historic_rates("ETH-USD", previous, now, 60)
    	raw_btc_entries = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

	#Replace Decimal with Decimal128 for mongo insertion
    	new_eth_entry = {k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in raw_eth_entries[0].items()}
    	new_btc_entry = {k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in raw_btc_entries[0].items()}

    	#Insert into mongo
    	eth_historical.insert_one(new_eth_entry)
    	btc_historical.insert_one(new_btc_entry)

    	now += datetime.timedelta(minutes=1)
    	previous += datetime.timedelta(minutes=1)

    	print("[HISTORICAL_INGESTION]: INGESTED BTC at " + str(datetime.datetime.now()))
    	print("[HISTORICAL_INGESTION]: INGESTED ETH at " + str(datetime.datetime.now()))

    	time.sleep(60)

#Start all threads
if __name__ == "__main__":
    #Init threads1
    time_diff_ingestion = threading.Thread(target=time_difference_ingestion, args=("time_diff", datetime.datetime.now()))
    live_ingestion = threading.Thread(target=live_ingestion, args=("live", datetime.datetime.now()))
    historical_ingestion = threading.Thread(target=historical_ingestion, args=("historical", datetime.datetime.now()))

    #Start threads
    time_diff_ingestion.start()
    live_ingestion.start()
    historical_ingestion.start()
