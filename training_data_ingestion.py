import pymongo
import datetime
import decimal
import time

import coinbasepro as cbp

from bson.decimal128 import Decimal128

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
cbp_client = cbp.PublicClient()

crypto_db = mongo_client['crypto']
eth_training_historical = crypto_db['eth_training_historical']
btc_training_historical = crypto_db['btc_training_historical']

now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

eth_training_historical.delete_many({})
btc_training_historical.delete_many({})

#Get past 25 days of 1 minute ticks
for x in range(0, 120):
	raw_eth_entries = cbp_client.get_product_historic_rates("ETH-USD", previous, now, 60)
	raw_btc_entries = cbp_client.get_product_historic_rates("BTC-USD", previous, now, 60)

	eth_entries = [{k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in i.items()} for i in raw_eth_entries]
	btc_entries = [{k: (Decimal128(v) if isinstance(v, decimal.Decimal) else v) for (k, v) in i.items()} for i in raw_btc_entries]

	eth_training_historical.insert_many(eth_entries)
	btc_training_historical.insert_many(btc_entries)

	print("[ETH_INGESTION_EPOCH]: " + str(x) + "Completed!")
	print("[BTC_INGESTION_EPOCH]: " + str(x) + "Completed!")

	now -= intervals
	previous -= intervals

	time.sleep(1)
