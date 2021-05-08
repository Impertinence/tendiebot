import pandas as pd
import numpy as np

import cudf

class Analyses():
    def __init__(self, dataset):
        self.dataset = pd.DataFrame(dataset)

    #Stochastics
    def stochastics(self, low, high, close, k, d):
        df = cudf.DataFrame.from_pandas(self.dataset)

        # Set min low and max high of stoch
        low_min = df[low].astype(float).rolling(window=k).min()
        high_max = df[high].astype(float).rolling(window=k).max()

        #Fast
        df['k_fast'] = 100 * (df[close].astype(float) - low_min)/(high_max - low_min)
        df['d_fast'] = df['k_fast'].rolling(window=d).mean()

        #Slow
        df['k_slow'] = df["d_fast"]
        df['d_slow'] = df["k_slow"].rolling(window=d).mean()

        return df

    #Moving Average Convergence Divergence
    def macd(self, fast_len, slow_len, src):
        df = self.dataset
        
        fast = df[src].ewm(span=fast_len, min_periods=1).mean()
        slow = df[src].ewm(span=slow_len, min_periods=1).mean()

        macd = fast - slow

        df['macd'] = macd
        df['signal'] = macd.ewm(span=9, adjust=False).mean()

        return df

    def ichimoku_cloud(self, rolling_period):
        df = cudf.DataFrame.from_pandas(self.dataset)

        nine_period_high = df['high'].rolling(window= int(rolling_period / 2)).max()
        nine_period_low = df['low'].rolling(window= int(rolling_period / 2)).min()

        ichimoku = (nine_period_high - nine_period_low) / 2
        ichimoku = ichimoku.replace([np.inf, -np.inf], np.nan)
        ichimoku = list(ichimoku.fillna(0.).values)

        return ichimoku

    def volatility_and_skew(self, rolling_period, src):
        df = cudf.DataFrame.from_pandas(self.dataset)

        #Volatility calcs
        volatility_1 = self.dataset[src].rolling(rolling_period).std()
        volatility_2 = self.dataset[src].rolling(rolling_period).var()

        volatility = volatility_1 / volatility_2

        #Rolling skewness (skew over rolling window)
        rolling_skewness = self.dataset[src].rolling(rolling_period).skew()
        rolling_kurtosis = self.dataset[src].rolling(rolling_period).kurt()

        df['volatility'] = volatility
        df['skewness'] = rolling_skewness
        df['kurtosis'] = rolling_kurtosis

        return df