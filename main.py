#Written by Pranav Hegde
import robin_stocks

from finance import interactions
from finance import analyses

#from storage import db_interactions

#Interactions
robinhood = interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")
market_analyses = analyses.Analyze()
#db = db_interactions.StockDB()

# print(robinhood.get_historicals(["tsla", "5minute", "week", "regular"])[0])
print(robinhood.get_current_price(["tsla"]))
