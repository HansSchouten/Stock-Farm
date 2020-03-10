
class Portfolio:
    """
    This class represents an investment portfolio.

    """

    def __init__(self, initialBalance: float):
        self.cashBalance = initialBalance
        self.totalValue = initialBalance

    def getValue(self):
        """
        Return the current total portfolio value.

        """
        return self.totalValue

    def buyLong(self, value):
        """
        Buy a long position for the given value.

        """
        if self.cashBalance < value:
            return

        self.cashBalance = self.cashBalance - value