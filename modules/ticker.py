
class StockTicker:
    """
    This class represents a list of stock market ticks.

    """

    def __init__(self, ticks: list, symbol = None):
        self.ticks = ticks
        self.symbol = symbol
        self.length = len(ticks)

    def getSymbol(self):
        """
        Return the symbol of the market this ticker represents.

        """
        return self.symbol

    def getLength(self):
        """
        Return the total number of ticks.

        """
        return self.length

    def get(self, index: int):
        """
        Return the ticker value at the given index.

        """
        return self.ticks[index]

    def getValues(self, key):
        """
        Return an array of all tick values for the given key.

        """
        values = []
        for tick in self.ticks:
            values.append(tick[key])
        return values


    def getHistoryWindow(self, width: int):
        """
        Return stock data from a given number of ticks in the past till now,
        or None if not enough ticks are present.

        """
        if width > self.length:
            return None

        ticks = []
        for windowIndex in range(width):
            tickIndex = self.length - width + windowIndex
            ticks.append(self.ticks[tickIndex])

        return StockTicker(ticks, self.symbol)