#Written by Pranav Hegde

import requests

from bs4 import BeautifulSoup

class StockInteractor():
    def get_analyses():
        print("asd")

    def get_stock(ticker, source):
        if(source == "yahoo"):
            url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker + "&.tsrc=fin-srch"
            r = requests.get(url)

            #Parse html
            soup = BeautifulSoup(r.text, 'html.parser')

            #Stock information
            current_price = float(soup.find("span", {"data-reactid": "50"}).string)
            open_price = float(soup.find("span", {"data-reactid", "98"}).string)
            year_range = float(soup.find("td", {"data-test", "FIFTY_TWO_WK_RANGE-value"}))
            
            print(year_range)
            
        return [
            current_price,
            open_price,
            year_range,
            week_range,

        ]

    def get_stock_historical(ticker, source):
        historical_data = []
        if(source == "yahoo"):
            url = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
            