
import sys

from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio
from pandas import DataFrame
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA as ARIMAModel
from sklearn.metrics import mean_squared_error

class ARIMA(Strategy):
    """
    This class represents an investment strategy based on ARIMA modelling.

    """

    def __init__(self, portfolio):
        self.previousValue = None
        self.prediction = None
        self.correctCount = 0
        return super().__init__(portfolio)

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        if self.prediction:
            if (self.prediction - tick['close'] < 0 and self.previousValue - tick['close'] < 0):
                self.correctCount = self.correctCount + 1                
            elif (self.prediction - tick['close'] > 0 and self.previousValue - tick['close'] > 0):
                self.correctCount = self.correctCount + 1
            print('Actual: %.3f' % (self.previousValue - tick['close']))
            print()

        recentHistory = ticker.getHistoryWindow(50)
        if recentHistory != None:
            historicValues = recentHistory.getValues('close')
            model = ARIMAModel(historicValues, order=(3,1,0))
            try:
                model_fit = model.fit(disp=0)
                self.prediction = model_fit.forecast()[0]
                self.previousValue = tick['close']
                print('Current value: %.3f' % tick['close'])
                print('Prediction: %.3f' % (self.prediction - tick['close']))
            except:
                pass

        if ticker.getLength() == 60:
            print(self.correctCount)
            sys.exit()

    def evaluatePredictions(self):
        """
        Compare historic data with predictions

        """
        history = ticker.getHistoryWindow(len(self.predictions)).getValues('close')
        error = mean_squared_error(history, self.predictions)
        print('Test MSE: %.3f' % error)
        pyplot.plot(history, color='black')
        pyplot.plot(self.predictions, color='blue')
        pyplot.show()
        sys.exit()

    def describeModel(self):
        """
        Describe the fitted ARIMA model.

        """
        print(self.model_fit.summary())

        residuals = DataFrame(self.model_fit.resid)
        residuals.plot()
        pyplot.show()
        residuals.plot(kind='kde')
        pyplot.show()
        print(residuals.describe())
