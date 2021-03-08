import pandas

class Analyses():
    def __init__(self, dataset):
        self.dataset = dataset

    def stochastics(self, low, high, close, k, d):
        df = self.dataset.copy()

        #Set min low and max high of stoch
        low_min = df[low].rolling(window=k).min()
        high_max = df[high].rolling(window=k).max()

        #Fast
        df['k_fast'] = 100 * (df[close] - low_min)/(high_max - low_min)
        df['d_fast'] = df['k_fast'].rolling(window=d).mean()

        #Slow
        df['k_slow'] = df["d_fast"]
        df['d_slow'] = df["k_slow"].rolling(window=d).mean()

        return df