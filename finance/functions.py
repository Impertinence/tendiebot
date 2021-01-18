class FinancialFunctions():
    def __init__(self, dataset):
        self.dataset = dataset

    #Exponential Moving Average
    def EMA(self, period):
        dataset = self.dataset
        for entry in dataset:
            print(entry)
