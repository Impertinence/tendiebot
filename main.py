import threading, time

from finance import data_generation, analyses

generate_data = data_generation.GenerateData()

#global vars
eth_hourly_data = []
eth_daily_data = []

def RetrieveHourlyCrypto(ticker):
    threading.Timer(15.0, RetrieveHourlyCrypto).start()
    eth_hourly_data = generate_data.PopulateCryptoHistorical([
        ticker,
        "15second",
        "hour",
        "24_7"
    ])

    recent_datapoint = eth_hourly_data[-1]
    new_analyse = analyses.GenerateAnalyses(eth_hourly_data).MACD()


def RetrieveDailyCrypto():
    threading.Timer(300.0, RetrieveDailyCrypto).start()
    eth_daily_data = generate_data.PopulateCryptoHistorical([
        "eth",
        "5minute",
        "day",
        "24_7"
    ])

#Init Ethereum retrieval
RetrieveHourlyCrypto("eth")
RetrieveDailyCrypto()
