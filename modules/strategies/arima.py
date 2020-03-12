
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
        print('[ Tick %i ]' % ticker.getLength())
        print('Closing price: %.3f' % tick['close'])

        if len(self.predictions) > 0:
            print('predicted=%f, expected=%f' % (self.predictions[len(self.predictions) - 1], tick['close']))

        if len(self.predictions) == 20:
            history = ticker.getHistoryWindow(20).getValues('close')
            print('Visualising...')
            print('History:')
            print(history)
            print('Predictions:')
            print(self.predictions)
            error = mean_squared_error(history, self.predictions)
            print('Test MSE: %.3f' % error)
            pyplot.plot(history, color='black')
            pyplot.plot(self.predictions, color='blue')
            pyplot.show()
            sys.exit()

        recentHistory = ticker.getHistoryWindow(20)
        if recentHistory != None:
            values  = recentHistory.getValues('close')
            model = ARIMAModel(values, order=(3,1,0))
            model_fit = model.fit(disp=0)
            forecast = model_fit.forecast()
            self.predictions.append(forecast[0][0])
            print('Forecasting for next iteration..')
            print(values)
            print('Forecast: %.3f' % forecast[0][0])

        print()

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
