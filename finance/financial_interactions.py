#Written by Pranav Hegde

import requests
import pymongo
import robin_stocks

from bson.json_util import dumps

# mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

# miscellaneous = mongo_client["miscellaneous"]
# robinhood_credentials = miscellaneous["rh_creds"]

class RobinHoodInteractions():
	def __init__(self, username, password):
		# rh_credentials = list(robinhood_credentials.find())
		# if(len(rh_credentials) == 0):
		# 	if(robinhood_credentials.insert_one(self.rh_account_info) != True):
		# 		print("error retrieving Robin Hood credentials...")

		self.rh_account_info = robin_stocks.authentication.login(username=username, password=password, expiresIn=86400, scope="internal", by_sms=True, store_session=True, mfa_code=None)
	
	def get_stock_historicals(self, params):
		return robin_stocks.get_stock_historicals(params[0], params[1], params[2], params[3])

	def get_current_price(self, tickers):
		return robin_stocks.stocks.get_quotes(tickers)

	def get_crypto_historicals(self, params):
		return robin_stocks.get_crypto_historicals(params[0], params[1], params[2], params[3])