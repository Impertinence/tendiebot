import threading, time

from finance import data_generation, analyses

generate_data = data_generation.GenerateData()

#global vars
hourly_data = []
daily_data = []

def RetrieveHourlyCrypto(ticker):
    threading.Timer(15.0, RetrieveHourlyCrypto, [ticker]).start()
    hourly_data = generate_data.PopulateCryptoHistorical([
        "eth",
        "15second",
        "hour",
        "24_7"
    ])

    new_analyse = analyses.GenerateAnalyses(hourly_data).MACD()


def RetrieveDailyCrypto(ticker):
    threading.Timer(300.0, RetrieveDailyCrypto, [ticker]).start()
    eth_daily_data = generate_data.PopulateCryptoHistorical([
        "eth",
        "5minute",
        "day",
        "24_7"
    ])

def run(ticker):
    RetrieveHourlyCrypto("eth")
    RetrieveDailyCrypto("eth")
#Init Ethereum retrieval
run("eth")
