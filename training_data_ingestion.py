import pymongo
import datetime
import decimal
import time

import coinbasepro as cbp

from bson.decimal128 import Decimal128

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
cbp_client = cbp.PublicClient()

crypto_db = mongo_client['crypto']
training_historicals = crypto_db['training_historicals']

now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

#Get past 25 days of 1 minute ticks
for x in range(0, 120):
	raw_entries = []

	eth_rates = [{**i, "asset": "ETH-USD"} for i in cbp_client.get_product_historic_rates("ETH-USD", previous, now, 60)]
	btc_rates = [{**i, "asset": "BTC-USD"} for i in cbp_client.get_product_historic_rates("BTC-USD", previous, now, 60)]

	
	raw_entries.extend(eth_rates)
	raw_entries.extend(btc_rates)

	d_comp1 = [{k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in i.items()} for i in raw_entries]
	entries = [{k: ((v - datetime.timedelta(hours=4)) if isinstance(v, datetime.datetime) else v) for (k, v) in i.items()} for i in d_comp1]

	training_historicals.insert_many(entries)

	print("[INGESTION_EPOCH]: " + str(x+1) + " Completed!")

	now -= intervals
	previous -= intervals

	time.sleep(1)