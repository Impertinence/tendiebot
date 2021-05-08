import pymongo
import threading
import time
import json

import datetime
import pandas as pd
import pymongo

from alpaca_trade_api.rest import REST, TimeFrame

api = REST()

class StockIngestion:
    def __init__(self):
        self.test = "test"

    #Ingest bars of data
    def ingest_bars(self, ticker, tframe):
        starting_time = datetime.date(2021, 1, 1).strftime("%Y-%m-%d")
        ending_time = datetime.date(2021, 1, 1).strftime("%Y-%m-%d")
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        frames = {"TICKER": ticker, "TFRAME": tframe}

        ingestion_start_time = datetime.datetime.now()

        #Ingest minute data
        while(ending_time < now and tframe == "min"):
            vals = api.get_bars(ticker, TimeFrame.Minute, starting_time, ending_time, limit=10000).df

            if (vals.empty != True):
                fmt_vals = json.loads(vals.to_json(orient="index"))
                {frames.update({key: fmt_vals[key]}) for key in fmt_vals}

            starting_time = (datetime.datetime.strptime(ending_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            ending_time = (datetime.datetime.strptime(ending_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            time.sleep(0.4)

        #Ingest hourly data
        while(ending_time < now and tframe == "hr"):
            vals = api.get_bars(ticker, TimeFrame.Hour, starting_time, ending_time, limit=10000).df

            if (vals.empty != True):
                fmt_vals = json.loads(vals.to_json(orient="index"))
                {frames.update({key: fmt_vals[key]}) for key in fmt_vals}

            starting_time = (datetime.datetime.strptime(ending_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            ending_time = (datetime.datetime.strptime(ending_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

            time.sleep(0.4)

        return frames