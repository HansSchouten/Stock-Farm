
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

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        recentHistory = ticker.getHistoryWindow(50)
        if recentHistory != None:
            historicValues = recentHistory.getValues('close')
            model = ARIMAModel(historicValues, order=(3,1,0))
            try:
                model_fit = model.fit(disp=0)
                closePrediction = model_fit.forecast()[0]
                deltaPrediction = closePrediction - tick['close']

                if deltaPrediction > 2:
                    print('Current stock value: %.3f' % tick['close'])
                    print('Prediction: %.3f' % deltaPrediction)
                    print('Buying stocks...')
                    amount = self.portfolio.calculateStockAmountFromBalancePercentage(tick['close'], 10)
                    cost = amount * tick['close']
                    self.portfolio.buyLong(ticker.getSymbol(), amount, cost, 1)
            except:
                return

        #if ticker.getLength() == 1000:
            #self.portfolio.printOverview()
            #sys.exit()

    def evaluatePredictions(self, predictions):
        """
        Compare historic data with predictions

        """
        history = ticker.getHistoryWindow(len(predictions)).getValues('close')
        error = mean_squared_error(history, predictions)
        print('Test MSE: %.3f' % error)
        pyplot.plot(history, color='black')
        pyplot.plot(predictions, color='blue')
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
