
from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class SimpleTrendStrategy(Strategy):
    """
    This class represents an investment strategy based on simple trend analysis.

    """

    def handleTick(self, ticker: StockTicker, tick: dict, portfolio: Portfolio):
        """
        Handle a new stock market tick.

        """