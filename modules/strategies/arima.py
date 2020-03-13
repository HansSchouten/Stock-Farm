
import sys

from modules.strategies.strategy import Strategy
from modules.ticker import StockTicker
from modules.portfolio import Portfolio
from pandas import DataFrame
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA as ARIMAModel
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")

class ARIMA(Strategy):
    """
    This class represents an investment strategy based on ARIMA modelling.

    """

    def handleTick(self, ticker: StockTicker, tick: dict):
        """
        Handle a new stock market tick.

        """
        #self.performTradingStrategy(ticker, tick)
        self.trainParameters(ticker, tick)

    def performTradingStrategy(self, ticker: StockTicker, tick: dict):
        """
        Perform trading strategy a new stock market tick.

        """
        recentHistory = ticker.getHistoryWindow(50)
        if recentHistory == None:
            return

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

        if ticker.getLength() == 1000:
            self.portfolio.printOverview()
            sys.exit()


    def trainParameters(self, ticker: StockTicker, tick: dict):
        """
        Train ARIMA model parameters.

        """
        recentHistory = ticker.getHistoryWindow(500)
        if recentHistory == None:
            return

        p_values = [0, 1, 2, 4, 6, 8, 10]
        d_values = range(0, 3)
        q_values = range(0, 3)
        best_score, best_cfg = float("inf"), None
        dataset = recentHistory.getValues('close')
        for p in p_values:
            for d in d_values:
                for q in q_values:
                    order = (p,d,q)
                    try:
                        mse = self.evaluateArimaModel(dataset, order)
                        if mse < best_score:
                            best_score, best_cfg = mse, order
                            print('ARIMA %s MSE=%.3f' % (order, mse))
                    except:
                        continue
        print('Best ARIMA %s MSE=%.3f' % (best_cfg, best_score))
        sys.exit()

    def evaluateArimaModel(self, X, arimaOrder):
        """
        Evaluate an ARIMA model for a given order (p,d,q).

        """
        # prepare training dataset
        train_size = int(len(X) * 0.66)
        train, test = X[0:train_size], X[train_size:]
        history = [x for x in train]
        # make predictions
        predictions = list()
        for t in range(len(test)):
            model = ARIMAModel(history, order=arimaOrder)
            model_fit = model.fit(disp=0)
            yhat = model_fit.forecast()[0]
            predictions.append(yhat)
            history.append(test[t])
        # calculate out of sample error
        error = mean_squared_error(test, predictions)
        return error

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
