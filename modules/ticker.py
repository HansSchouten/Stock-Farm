
class StockTicker:
    """
    This class represents a list of stock market ticks.

    """

    def __init__(self, ticks: list):
        self.ticks = ticks

    def getLength(self):
        """
        Return the total number of ticks.

        """
        return len(self.ticks)

    def get(self, index: int):
        """
        Return the ticker value at the given index.

        """
        return self.ticks[index]