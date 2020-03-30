
class Portfolio:
    """
    This class represents an investment portfolio.

    """

    def __init__(self, initialBalance: float):
        self.cashBalance = initialBalance
        self.investments = []
        self.newInvestments = []
        self.openFeeFactor = 0.1 / 100
        self.closeFeeFactor = 0.1 / 100

    def getValue(self):
        """
        Return the total portfolio value.

        """
        return self.cashBalance

    def getPositions(self):
        """
        Return all currently active positions.

        """
        return self.investments

    def processAfterTick(self, symbol, closeValue):
        """
        Close investments that triggered stop losses or that reached their max duration.

        """
        investmentsAfterTick = []
        for investment in self.investments:
            if investment['symbol'] == symbol and 'maxTicksLeft' in investment:
                investment['maxTicksLeft'] = investment['maxTicksLeft'] - 1
                if investment['maxTicksLeft'] == 0:
                    print('Sold due to timeout:')
                    print(closeValue)
                    self.closePosition(investment, closeValue)
                else:
                    investmentsAfterTick.append(investment)
            else:
                investmentsAfterTick.append(investment)
        self.investments = investmentsAfterTick

        # move new investments (made during the current tick) to the list of all currently open investments
        newInvestmentsOfOtherSymbols = []
        for investment in self.newInvestments:
            if investment['symbol'] == symbol:
                self.investments.append(investment)
            else:
                newInvestmentsOfOtherSymbols.append(investment)
        self.newInvestments = newInvestmentsOfOtherSymbols

    def calculateStockAmountFromBalancePercentage(self, stockValue, percentage):
        """
        Return amount of shares of the given current stock price to invest if we want to use a percentage of our current cash balance.

        """
        return ((percentage / 100) * self.cashBalance) / stockValue

    def buyLong(self, symbol, amount, initialValue, maxTicksDuration = None):
        """
        Buy a long position for the given amount of stocks.

        """
        cost = initialValue * (1 + self.openFeeFactor)

        if self.cashBalance <= cost:
            return

        investment = {}
        investment['type'] = 'long'
        investment['symbol'] = symbol
        investment['initialValue'] = initialValue
        investment['amount'] = amount
        if maxTicksDuration is not None:
            investment['maxTicksLeft'] = maxTicksDuration
        self.newInvestments.append(investment)
        self.cashBalance = self.cashBalance - cost

    def closePosition(self, investment, marketValue):
        """
        Close a given position against the given market value.

        """
        if investment['type'] == 'long':
            closeValue = investment['amount'] * marketValue * (1 - self.closeFeeFactor)
            print(str(round(investment['initialValue'], 2)) + " -> " + str(round(closeValue, 2)))
            print(marketValue)
            self.cashBalance = self.cashBalance + closeValue

    def closeAllPositions(self, symbol, marketValue):
        """
        Close all positions in the given market against the given market value.

        """
        investmentsOfOtherSymbols = []
        for investment in self.investments:
            if investment['symbol'] == symbol:
                self.closePosition(investment, marketValue)
            else:
                investmentsOfOtherSymbols.append(investment)

        self.investments = investmentsOfOtherSymbols

    def printOverview(self):
        """
        Print the current portfolio.

        """
        print('Cash balance: %.3f' % self.cashBalance)