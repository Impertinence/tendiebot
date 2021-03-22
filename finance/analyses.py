import pandas as pd

class Analyses():
    def __init__(self, dataset):
        self.dataset = dataset

    #Stochastics
    def stochastics(self, low, high, close, k, d):
        df = pd.DataFrame(self.dataset)

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

    def macd():