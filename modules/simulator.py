
from modules.parsers import YahooFinanceParser

class MarketSimulator:
    '''
    This class simulates a stock market of a particular symbol.

    '''

    def __init__(self, symbol):
        self.symbol = symbol
        self.parser = YahooFinanceParser(symbol)

class StrategySimulator:
    '''
    This class simulates an investment strategy on a given stock market.

    '''

    def __init__(self, market, strategy):
        self.market = market
        self.strategy = strategy