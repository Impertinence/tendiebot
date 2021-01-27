import pymongo

from finance import yahoo, analyses, financial_interactions

yh = yahoo.YahooInteractions()
fi = financial_interactions.RobinHoodInteractions("pranavhegde11@gmail.com", "ae0iuwRmna1851")

day_gainers = yh.get_day_gainers()
day_losers = yh.get_day_losers()