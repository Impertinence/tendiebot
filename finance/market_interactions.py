#Written by Pranav Hegde

import requests
import pymongo
import robin_stocks
import bs4

from bson.json_util import dumps

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

miscellaneous = mongo_client["miscellaneous"]
robinhood_credentials = miscellaneous["rh_creds"]

class YahooInteractions():
	def get_stock(ticker):
        url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
        r = requests.get(url)

        #Parse html
        soup = BeautifulSoup(r.text, 'html.parser')

    	#Stock information
        current_price = float(soup.find("span", {"data-reactid": "50"}).string)
        open_price = float(soup.find("span", {"data-reactid", "98"}).string)
        #year_range = float(soup.find("td", {"data-test", "FIFTY_TWO_WK_RANGE-value"}))
            
        print(year_range)
            
        return [
            current_price,
            open_price
        ]

class RobinHoodInteractions():
	def __init__(self, username, password):
		rh_credentials = list(robinhood_credentials.find())
		if(len(rh_credentials) == 0):
			if(robinhood_credentials.insert_one(self.rh_account_info) != True):
				print("error retrieving Robin Hood credentials...")

		self.rh_account_info = robin_stocks.authentication.login(username=username, password=password, expiresIn=86400, scope="internal", by_sms=True, store_session=True, mfa_code=None)
