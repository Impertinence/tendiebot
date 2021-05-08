import pymongo
import time
import threading
import datetime

from finance import analyses

from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from decimal import Decimal

import json

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")

#DB access
crypto_db = mongo_client['crypto']
trading_db = mongo_client['trading']

#Data Collections
btc_historical = crypto_db['btc_historical']
eth_historical = crypto_db['eth_historical']
live_crypto = crypto_db['live']

#Trading Collections
crypto_trading = trading_db['crypto']

current_eth_sentiment = None
current_btc_sentiment = None

#Financial
simulated_account = open("files/sim_account.json").read()

balance = simulated_account['']

#Minute-by-Minute analysis
def MinuteAnalysis(thread_name, time_rn):
	while True:
		current_btc_historicals = list(btc_historical.find())
		current_eth_historicals = list(eth_historical.find())

		#btc
		btc_d_comp = [{k: (str(v) if isinstance(v, ObjectId) else v) for (k, v) in i.items()} for i in current_btc_historicals]
		btc_actual = [{k: (float(str(v)) if isinstance(v, Decimal128) else v) for (k, v) in i.items()} for i in eth_d_comp]

		#eth
		eth_d_comp = [{k: (str(v) if isinstance(v, ObjectId) else v) for (k, v) in i.items()} for i in current_eth_historicals]
		eth_actual = [{k: (float(str(v)) if isinstance(v, Decimal128) else v) for (k, v) in i.items()} for i in eth_d_comp]

		#Analyses
		btc_analysis = analyses.Analyses(btc_actual)
		eth_analysis = analyses.Analyses(eth_actual)

		btc_stochs =  btc_analysis.stochastics("low", "high", "close", 14, 3)
		eth_stochs = eth_analysis.stochastics("low", "high", "close", 14, 3)
		btc_macd = btc_analysis.macd(12, 26, 'close')
		eth_macd = eth_analysis.macd(12, 26, 'close')

		time.sleep(60)

#Second by Second analysis
def SecondAnalysis(thread_name, time_rn):
	while True:
		live_crypto_vals = list(live_crypto.find())

		time.sleep(1)

if __name__ == "__main__":
	minute_analysis = threading.Thread(target=MinuteAnalysis, args=("min", datetime.datetime.now()))
	second_analysis = threading.Thread(target=SecondAnalysis, args=("sec", datetime.datetime.now()))

	minute_analysis.start()
	second_analysis.start()