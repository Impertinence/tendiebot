
#Basic financial functions
def SMA(dataset, periods):
    chunk_size = int(len(dataset)/periods)
    i = 0
    total_value = 0

    #Iterate through dataset and retrieve price values specified by period
    while(i < int(len(dataset))):
        pricepoint = dataset[i]

        #Entry details
        open_price = float(pricepoint['open_price'])
        close_price = float(pricepoint['close_price'])
        max_price_range = float(pricepoint['high_price']) - float(pricepoint['low_price'])
        total_price_range = float(pricepoint['open_price']) - float(pricepoint['close_price'])

        total_value+=close_price
        i+=chunk_size
    
    return total_value/periods

def EMA(dataset, previous_ma, periods):
    chunk_size = len(dataset)/periods

    initial_ema = SMA(dataset, periods)


class GenerateAnalyses():
    def __init__(self, dataset):
        self.dataset = dataset

    #Moving Average Convergence Divergence
    def MACD(self):
        dataset = self.dataset
        ema = EMA(dataset, 12)