
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
    buyingType = None
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
            self.portfolio.closeAllPositions(ticker.getSymbol(), tick[self.buyingType])

        if len(self.portfolio.getPositions()) > 0:
            return
        
        # buy with delay
        if self.hasBuyBullTrigger(recentHistory) and self.sellingDelayCountdown == -1 and self.buyingDelayCountdown == -1 and len(self.portfolio.getPositions()) == 0:
            self.buyingDelayCountdown = self.buyingDelay
            self.buyingType = "bull"

        if self.hasBuyBearTrigger(recentHistory) and self.sellingDelayCountdown == -1 and self.buyingDelayCountdown == -1 and len(self.portfolio.getPositions()) == 0:
            self.buyingDelayCountdown = self.buyingDelay
            self.buyingType = "bear"

        if self.buyingDelayCountdown == 0:
            print('Buy ' + self.buyingType + ":")
            print(tick)
            amount = self.portfolio.calculateStockAmountFromBalancePercentage(tick[self.buyingType], 90)
            self.portfolio.buyLong(ticker.getSymbol(), amount, amount * tick[self.buyingType])
            self.sellingDelayCountdown = 10
                
    def hasBuyBullTrigger(self, recentHistory):
        """
        Check whether the bullish buying condition has triggered.

        """
        predictorValues = recentHistory.getValues("btc")
        followerValues = recentHistory.getValues("bull")
        triggered = predictorValues[4] - predictorValues[3] > 0.0012 * predictorValues[3] \
            and followerValues[0] == followerValues[4]
            #and ((followerValues[0] + followerValues[1] + followerValues[2] + followerValues[3] + followerValues[4]) / 5) <= followerValues[4] \
            #and abs(followerValues[4] - followerValues[0]) < 0.005 * followerValues[4]
        if (triggered):
            print()
            print("BTC:")
            print(predictorValues)
            print("ETHBULL:")
            print(followerValues)
        return triggered
                
    def hasBuyBearTrigger(self, recentHistory):
        """
        Check whether the bearish buying condition has triggered.

        """
        predictorValues = recentHistory.getValues("btc")
        followerValues = recentHistory.getValues("bear")
        triggered = predictorValues[4] - predictorValues[3] < -0.0012 * predictorValues[3] \
            and followerValues[0] == followerValues[4]
            #and ((followerValues[0] + followerValues[1] + followerValues[2] + followerValues[3] + followerValues[4]) / 5) <= followerValues[0] \
            #and abs(followerValues[4] - followerValues[0]) < 0.005 * followerValues[4]
        if (triggered):
            print()
            print("BTC:")
            print(predictorValues)
            print("ETHBEAR:")
            print(followerValues)
        return triggered

    def hasToClose(self, recentHistory, tick, position):
        """
        Check whether we have to close the given position.

        """
        currentValue = position['amount'] * tick[self.buyingType]
        return currentValue > (position['initialValue'] * 1.01)# or currentValue < (position['initialValue'] * 0.99)