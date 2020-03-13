
class Portfolio:
    """
    This class represents an investment portfolio.

    """

    def __init__(self, initialBalance: float):
        self.cashBalance = initialBalance
        self.investments = []
        self.newInvestments = []

    def getValue(self):
        """
        Return the total portfolio value.

        """
        return self.cashBalance

    def processAfterTick(self, symbol, minValue, maxValue, closeValue):
        """
        Close investments that triggered stop losses or that reached their max duration.

        """
        investmentsAfterTick = []
        for investment in self.investments:
            if investment['symbol'] == symbol:
                investment['maxTicksLeft'] = investment['maxTicksLeft'] - 1
                if investment['maxTicksLeft'] == 0:
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

    def buyLong(self, symbol, amount, cost, maxTicksDuration):
        """
        Buy a long position for the given amount of stocks.

        """
        if self.cashBalance < cost:
            return

        investment = {}
        investment['type'] = 'long'
        investment['symbol'] = symbol
        investment['amount'] = amount
        investment['maxTicksLeft'] = maxTicksDuration
        self.newInvestments.append(investment)
        self.cashBalance = self.cashBalance - cost

    def closePosition(self, investment, marketValue):
        """
        Close a given position against the given market value.

        """
        if investment['type'] == 'long':
            self.cashBalance = self.cashBalance + (investment['amount'] * marketValue)

    def closeAllPositions(self, symbol, marketValue):
        """
        Close all positions in the given market against the given market value.

        """
        investmentsOfOtherSymbols = []
        for investment in self.investments:
            if investment['symbol'] == symbol:
                if investment['type'] == 'long':
                    self.cashBalance = self.cashBalance + (investment['amount'] * marketValue)
            else:
                investmentsOfOtherSymbols.append(investment)

        self.investments = investmentsOfOtherSymbols

    def printOverview(self):
        """
        Print the current portfolio.

        """
        print('Cash balance: %.3f' % self.cashBalance)