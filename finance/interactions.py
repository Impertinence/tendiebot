import requests
import websockets
import asyncio
import pymongo
import robin_stocks

from bson.json_util import dumps
from bs4 import BeautifulSoup
from itertools import groupby

#Yahoo finance access
class YAHOO():
    def __init__(self):
        self.test = "2"

    #Get Day Gainers
    def get_day_gainers(self):
        r = requests.get("https://finance.yahoo.com/screener/predefined/day_gainers")

        #HTML Manipulation (ugly shit)
        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("tbody", {"data-reactid": "72"}).find_all('td')]

        #Easier than I thought lol
        #Reorganize data and return
        return [list(group) for k, group in groupby(keys, lambda x: x == "") if not k]
    
    #Get Day Losers
    def get_day_losers(self):
        r = requests.get("https://finance.yahoo.com/screener/predefined/day_losers")

        #HTML Manipulation (ugly shit)
        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("tbody", {"data-reactid": "72"}).find_all('td')]

        #Easier than I thought lol
        #Reorganize data and return
        return [list(group) for k, group in groupby(keys, lambda x: x == "") if not k]

    #Get historicals
    def get_historicals(self, ticker):
        r = requests.get("https://finance.yahoo.com/quote/" + ticker.upper() + "/history?p=" + ticker.upper())

        #HTML Manipulation (ugly shit)
        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("tbody").find_all('td')]
        
        #Reorganize data and return
        results = []
        i = 0
        while i < (len(keys)):
            results.append(keys[(i-7):i])
            i+=7

        #Convert entries to dict (mongodb only enters dicts)
        result_dict = []
        for i in results:
            print(i)


#Finnhub access
class FINNHUB():
    def __init__(self):
        self.sandbox_key = "sandbox_c0dene748v6sgrj2gf50"
        self.api_key = "c0dene748v6sgrj2gf4g"

    #Realtime price quote
    def realtime_quote(self, ticker):
        r = requests.get('https://www.finnhub.io/api/v1/quote?symbol=' + ticker.upper() + '&token=' + self.api_key)
        return r.json()

    #Financial Headlines
    def company_news(self, ticker, starting, ending):
        r = requests.get('https://www.finnhub.io/api/v1/company-news?symbol=' + ticker.upper() + "&from=" + starting + "&to=" + ending + "&token=" + self.api_key)
        return r.json()

    #Support/resistance level
    def support_resistance(self, ticker, res):
        r = requests.get('https://www.finnhub.io/api/v1/scan/support-resistance?symbol=' + ticker.upper() + '&resolution=' + res + "&token=" + self.api_key)
        return r.json()

    # Pattern recognition
    def pattern_recognition(self, ticker, res):
        r = requests.get('https://www.finnhub.io/api/v1/scan/pattern?symbol=' + ticker.upper() + '&resolution=' + res + "&token=" + self.api_key)
        return r.json()

#Openinsider access
class OPENINSIDER():
    def __init__(self):
        self.uri = "http://www.openinsider.com/screener?s="
    
    def get_insider_transactions(self, ticker):
        r = requests.get(self.uri + ticker)

        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("table", {"class": "tinytable"}).find_all("td")]
        
        return [list(group) for k, group in groupby(keys, lambda x: x == "") if not k]

#Robinhood access
class ROBINHOOD():
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

	def get_watchlists(self):
		return robin_stocks.account.get_all_watchlists()

#marketwatch access
class MARKETWATCH():
    def __init__(self):
        self.uri = ""

    def getSmallCap(self):
        tickers = []
        for x in range(0, 44):
            r = requests.get("https://www.marketwatch.com/tools/stockresearch/screener/results.asp?TradesShareEnable=True&TradesShareMin=0&TradesShareMax=25&PriceDirEnable=False&PriceDir=Up&LastYearEnable=False&TradeVolEnable=False&TradeVolMin=0&TradeVolMax=100000000&BlockEnable=False&PERatioEnable=False&MktCapEnable=False&MovAvgEnable=False&MovAvgType=Outperform&MovAvgTime=FiftyDay&MktIdxEnable=False&MktIdxType=Outperform&Exchange=All&IndustryEnable=False&Industry=Accounting&Symbol=True&CompanyName=True&Price=True&Change=True&ChangePct=True&Volume=True&LastTradeTime=False&FiftyTwoWeekHigh=False&FiftyTwoWeekLow=False&PERatio=False&MarketCap=False&MoreInfo=True&SortyBy=Symbol&SortDirection=Ascending&ResultsPerPage=OneHundred&PagingIndex=" + str(x*100))

            soup = BeautifulSoup(r.text, 'html.parser')
            keys = [i.text for i in soup.find("tbody").find_all('td')]
            results = [list(group) for k, group in groupby(keys, lambda x: x == "chart\xa0news") if not k]

            for z in results:
                tickers.append(z[0])
        return tickers
