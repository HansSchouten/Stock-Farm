
import sys
import random
from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio

class HFT(Strategy):
    """
    This class represents an investment strategy based on High Frequency Trading.

    """

    buyingDelay = 1
    sellingDelay = 1
    buyingDelayCountdown = -1
    sellingDelayCountdown = -1

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        recentHistory = ticker.getHistoryWindow(5)

        if recentHistory is None:
            return
            
        # decrease buy/sell delay countdowns
        if self.buyingDelayCountdown >= 0:
            self.buyingDelayCountdown = self.buyingDelayCountdown - 1
        if self.sellingDelayCountdown >= 0:
            self.sellingDelayCountdown = self.sellingDelayCountdown - 1
        
        # sell with delay
        for position in self.portfolio.getPositions():
            if self.hasToClose(recentHistory, tick, position) and self.sellingDelayCountdown == -1 and self.buyingDelayCountdown == -1:
                self.sellingDelayCountdown = self.sellingDelay

        if self.sellingDelayCountdown == 0:
            print('Sell:')
            print(tick)
            self.portfolio.closeAllPositions(ticker.getSymbol(), tick['bull'])
        
        # buy with delay
        if self.hasBuyTrigger(recentHistory) and self.sellingDelayCountdown == -1 and self.buyingDelayCountdown == -1 and len(self.portfolio.getPositions()) == 0:
            self.buyingDelayCountdown = self.buyingDelay

        if self.buyingDelayCountdown == 0:
            print()
            print('Buy:')
            print(tick)
            amount = self.portfolio.calculateStockAmountFromBalancePercentage(tick['bull'], 90)
            self.portfolio.buyLong(ticker.getSymbol(), amount, amount * tick['bull'], 600)
                
    def hasBuyTrigger(self, recentHistory):
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
        return currentValue > (position['initialValue'] * 1.005)