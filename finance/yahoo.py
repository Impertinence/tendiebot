import requests

from bs4 import BeautifulSoup
from itertools import groupby


class YahooInteractions():
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