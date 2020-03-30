
import sys
import random
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
        recentHistory = ticker.getHistoryWindow(5)

        if recentHistory is None:
            return
        
        if self.hasTriggered(recentHistory):
            amount = self.portfolio.calculateStockAmountFromBalancePercentage(tick['bull'], 30)
            initialValue = amount * tick['bull']
            self.portfolio.buyLong(ticker.getSymbol(), amount, initialValue)

        for position in self.portfolio.getPositions():
            if self.hasToClose(recentHistory, tick, position):
                self.portfolio.closeAllPositions(ticker.getSymbol(), tick['bull'])
                
    def hasTriggered(self, recentHistory):
        """
        Check whether the buying condition has triggered.

        """
        predictorValues = recentHistory.getValues("btc")
        return predictorValues[4] - predictorValues[3] > 0.001 * predictorValues[3]

    def hasToClose(self, recentHistory, tick, position):
        """
        Check whether we have to close the given position.

        """
        currentValue = position['amount'] * tick['bull']
        if currentValue > (position['initialValue'] * 1.01):
            print(str(position['initialValue']) + " -> " + str(currentValue))
            return True
        return False