import requests
import websockets
import asyncio

from bs4 import BeautifulSoup
from itertools import groupby


class YAHOO():
    def __init__(self):
        self.test = "2"

    def get_day_gainers(self):
        r = requests.get("https://finance.yahoo.com/screener/predefined/day_gainers")

        #HTML Manipulation (ugly shit)
        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("tbody", {"data-reactid": "72"}).find_all('td')]

        #Easier than I thought lol
        #Reorganize data and return
        return [list(group) for k, group in groupby(keys, lambda x: x == "") if not k]
    
    def get_day_losers(self):
        r = requests.get("https://finance.yahoo.com/screener/predefined/day_gainers")

        #HTML Manipulation (ugly shit)
        soup = BeautifulSoup(r.text, 'html.parser')
        keys = [i.text for i in soup.find("tbody", {"data-reactid": "72"}).find_all('td')]

        #Easier than I thought lol
        #Reorganize data and return
        return [list(group) for k, group in groupby(keys, lambda x: x == "") if not k]

class FINNHUB():
    def __init__(self):
        self.sandbox_key = "sandbox_c0dene748v6sgrj2gf50"
        self.api_key = "c0dene748v6sgrj2gf4g"

    def realtime_quote(self, ticker):
        r = requests.get('https://www.finnhub.io/api/v1/quote?symbol=' + ticker.upper() + '&token=' + self.api_key)
        return r.json()

