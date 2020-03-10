
class Portfolio:
    """
    This class represents an investment portfolio.

    """

    def __init__(self, initialBalance: float):
        self.totalValue = initialBalance

    def getValue(self):
        """
        Return the current total portfolio value.

        """
        return self.totalValue