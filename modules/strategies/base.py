
from abc import ABC, abstractmethod
from modules.investments import Portfolio

class Strategy(ABC):
    """
    This abstract class defines the base class structure of any strategy.

    """

    @abstractmethod
    def handleTick(self, portfolio: Portfolio, tick: dict):
        """
        Handle a new stock market tick.

        """
        pass