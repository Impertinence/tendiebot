
#Basic financial functions
def EMA(dataset, periods):
    print(dataset[-1]['open_price'])

class GenerateAnalyses():
    def __init__(self, dataset):
        self.dataset = dataset

    def MACD(self):
        dataset = self.dataset
        ema = EMA(dataset, 12)