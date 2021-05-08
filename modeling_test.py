import pymongo
import matplotlib.pyplot as plt
import datetime

import pandas as pd
import numpy as np

from finance import analyses
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from decimal import Decimal

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")

crypto_db = mongo_client['crypto']

#Collections
live = crypto_db['live']
historical = crypto_db['training_historicals']

start_time = datetime.datetime.now()

#Manipulate mongo returns
d_comp = [{k: (str(v) if isinstance(v, ObjectId) else v) for (k, v) in i.items()} for i in list(historical.find())]
training_historicals = [{k: (float(str(v)) if isinstance(v, Decimal128) else v) for (k, v) in i.items()} for i in d_comp]

ROLLING = 30
WINDOW = 30
STEP = 1
FORECAST = 14
TEST_SET = 0.9

#Raw Training Data
eth_historical = [i for i in training_historicals if i['asset'] == "ETH-USD"]
# btc_df = cudf.from_pandas.DataFrame(pd.DataFrame([i for i in training_historicals if i['asset'] == "BTC-USD"]))

#Analyses objects
eth_analysis = analyses.Analyses(eth_historical)

#Indicators
ichimoku = eth_analysis.ichimoku_cloud(ROLLING)
stochs = eth_analysis.stochastics('low', 'high', 'close', 14, 3)
macd = eth_analysis.macd(12, 6, 'close')
skewness = eth_analysis.volatility_and_skew(ROLLING, 'close')

X_TRAIN, X

# fig, axs = plt.subplots(nrows=3)
# axs[0].plot(list(skewness['time'].to_pandas()), list(skewness['close'].to_pandas()))
# axs[1].plot(list(skewness['time'].to_pandas()), list(skewness['skewness'].to_pandas()))
# axs[2].plot(list(skewness['time'].to_pandas()), list(stochs['k_slow'].to_pandas()))
# axs[2].plot(list(skewness['time'].to_pandas()), list(stochs['d_slow'].to_pandas()))

plt.show()
print(datetime.datetime.now() - start_time)