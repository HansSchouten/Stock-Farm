
from abc import ABC, abstractmethod
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class Strategy(ABC):
    """
    This abstract class defines the base class structure of any strategy.

    """

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    @abstractmethod
    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        pass


class NothingStrategy(Strategy):
    """
    This class represents an investment strategy that does not perform any trades.

    """

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """