
from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class SimpleTrendStrategy(Strategy):
    """
    This class represents an investment strategy based on simple trend analysis.

    """

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        recentHistory = ticker.getHistoryWindow(20)
        if recentHistory != None:
            if self.isUpwardTrend(recentHistory):
                amount = self.portfolio.calculateStockAmountFromBalancePercentage(tick['close'], 10)
                cost = amount * tick['close']
                self.portfolio.buyLong(ticker.getSymbol(), amount, cost, 10)

    def isUpwardTrend(self, history: StockTicker):
        """
        Return whether the given history shows an upward trend.

        """
        upwardCount = 0
        for i in range(1, history.getLength()):
            previousTick = history.get(i - 1)['close']
            thisTick = history.get(i)['close']
            if thisTick != None and previousTick != None and history.get(i)['close'] > history.get(i-1)['close']:
                upwardCount = upwardCount + 1

        return upwardCount > (history.getLength() / 2)