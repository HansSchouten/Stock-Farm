
'''
This class simulates a stock market of a particular symbol.
'''
class MarketSimulator:
    def __init__(self, symbol):
        self.symbol = symbol

'''
This class simulates an investment strategy on the stock market.
'''
class StrategySimulator:
    def __init__(self, market, strategy):
        self.market = market
        self.strategy = strategy