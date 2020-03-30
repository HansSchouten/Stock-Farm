
from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class HFT(Strategy):
    """
    This class represents an investment strategy based on High Frequency Trading.

    """

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        print(tick)