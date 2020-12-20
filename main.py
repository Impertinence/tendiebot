from finance import market_interactions
import time
import pymongo

start_time = time.time()
market_interactions = market_interactions.Main()

print(market_interactions.get_stock("tsla", "yahoo"))
print("time: " + (time.time() - start_time) + " seconds")