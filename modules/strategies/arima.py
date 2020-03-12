
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
        self.predictions = []
        return super().__init__(portfolio)

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        if len(self.predictions) > 0:
            print('predicted=%f, expected=%f' % (self.predictions[len(self.predictions)-1], tick['close']))

        if len(self.predictions) == 100:
            history = ticker.getHistoryWindow(100).getValues('close')
            error = mean_squared_error(history, self.predictions)
            print('Test MSE: %.3f' % error)
            pyplot.plot(history)
            pyplot.plot(self.predictions, color='red')
            pyplot.show()
            sys.exit()

        recentHistory = ticker.getHistoryWindow(100)
        if recentHistory != None:
            values  = recentHistory.getValues('close')
            model = ARIMAModel(values, order=(3,2,0))
            model_fit = model.fit(disp=0)
            forecast = model_fit.forecast()[0]
            self.predictions.append(forecast)

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
