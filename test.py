from finance import market_interactions
import csv

oi = market_interactions.OPENINSIDER()
yh = market_interactions.YAHOO()
mw = market_interactions.MARKETWATCH()

# all_smallcap = mw.getSmallCap()

# with open('files/all_smallcap.csv', 'w') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(all_smallcap)

print(yh.get_historicals("gme"))

