import pymongo
import coinbasepro as cbp

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
cbp_client = cbp.PublicClient()

crypto_db = mongo_client['crypto']
eth_training_historical = crypto_db['eth_training_historical']
btc_training_historical = crypto_db['btc_training_historical']

now = datetime.datetime.now() + datetime.timedelta(hours=4)
intervals = datetime.timedelta(minutes=300)
previous = now - intervals

training_historicals.delete_many({})

for x in range(0, 120):
	eth_entries = cbp_client.get_product_historic_rates("ETH-USD", previous, now, 60)
	btc_entries = cbp_client.get_product_historic_rates("BTC-USD", previous, now, 60)

	eth_training_historical.insert_many(eth_entries)
	btc_training_historical.insert_many(btc_entries)

	print("[ETH_INGESTION_EPOCH]: " + x)
	print("[BTC_INGESTION_EPOCH]: " + x)

	now -= intervals
	previous -= intervals

	time.sleep(0.4)
