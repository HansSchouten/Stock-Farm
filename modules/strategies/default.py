
from modules.strategies.base import Strategy
from modules.investments import Portfolio

class DefaultStrategy(Strategy):
    """
    This class represents an empty base strategy.

    """

    def handleTick(self, portfolio: Portfolio, tick: dict):
        """
        Handle a new stock market tick.

        """