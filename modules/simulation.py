
from modules.parsers import YahooFinanceParser
from modules.strategies.strategy import Strategy
from modules.portfolio import Portfolio
from modules.ticker import StockTicker

class MarketSimulator:
    """
    This class simulates a stock market of a particular stock symbol.

    """

    def __init__(self, symbol: str):
        parser = YahooFinanceParser()
        self.ticker = parser.getTicker(symbol)
        self.symbol = symbol
        self.currentTickIndex = 0
        self.tickerLength = self.ticker.getLength()
        self.history = []

    def hasNext(self):
        """
        Return whether the market has more ticks.

        """
        return self.currentTickIndex < (self.tickerLength - 1)

    def getNext(self):
        """
        Return the next tick of the simulated stock market.

        """
        tick = self.ticker.get(self.currentTickIndex)
        self.history.append(tick)
        self.currentTickIndex = self.currentTickIndex + 1
        return tick

    def getHistory(self):
        """
        Return the ticker of this market up to the currently simulated moment.

        """
        return StockTicker(self.history)


class StrategySimulator:
    """
    This class simulates an investment strategy on a given stock market.

    """

    def __init__(self, marketSimulator: MarketSimulator, strategy: Strategy, portfolio: Portfolio):
        self.marketSimulator = marketSimulator
        self.strategy = strategy
        self.portfolio = portfolio

    def run(self):
        """
        Simulate the strategy in the stock market simulator.

        """
        while self.marketSimulator.hasNext():
            tick = self.marketSimulator.getNext()
            self.strategy.handleTick(self.marketSimulator.getHistory(), tick, self.portfolio)