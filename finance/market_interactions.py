#Written by Pranav Hegde

import requests
import pymongo
import robin_stocks

class RobinHoodInteractions():
	def __init__(self, username, password, expiresIn, scope, by_sms, store_session, mfa_code):
		self.account_info = robin_stocks.authentication.login(username, password, expiresIn, scope, by_sms, store_session, mfa_code)
