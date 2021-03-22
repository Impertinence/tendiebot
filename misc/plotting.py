import matplotlib.pyplot as plt

class Plot:
    def __init__(self, dataset):
        self.dataset = dataset

    #Plot stochastics
    def stochastics(self):
        dataset = self.dataset

        time = dataset['time'].to_list()
        l = dataset['low'].to_list()
        h = dataset['high'].to_list()
        o = dataset['open'].to_list()
        c = dataset['close'].to_list()

        #Stochastics
        k_fast = dataset['k_fast'].to_list()
        k_slow = dataset['k_slow'].to_list()
        d_fast = dataset['d_fast'].to_list()
        d_slow = dataset['d_slow'].to_list()

        plt.plot(time, k_fast)
        plt.plot(time, d_fast)

        plt.show()