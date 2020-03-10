
from abc import ABC, abstractmethod
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class Strategy(ABC):
    """
    This abstract class defines the base class structure of any strategy.

    """

    @abstractmethod
    def handleTick(self, ticker: StockTicker, tick: dict, portfolio: Portfolio):
        """
        Handle a new stock market tick.

        """
        pass


class NothingStrategy(Strategy):
    """
    This class represents an investment strategy that does not perform any trades.

    """

    def handleTick(self, portfolio: Portfolio, tick: dict):
        """
        Handle a new stock market tick.

        """