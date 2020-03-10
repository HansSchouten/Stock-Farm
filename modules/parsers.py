
import sys
import json
import datetime

from pathlib import Path
from modules.time_series import StockTicker

class YahooFinanceParser:
    """
    This class parses historic stock data from Yahoo Finance.

    """

    def getTicker(self, symbol):
        """
        Read the json file of the configured stock market and return a list of ticks.

        """
        dataFilePath = Path('data/' + symbol + '.json')

        if not dataFilePath.is_file():
            print('File ' + str(dataFilePath) + ' not found!')
            sys.exit(2)

        ticks = []
        with open(dataFilePath) as dataFile:
            data = json.load(dataFile)

            for i, unixTimestamp in enumerate(data['chart']['result'][0]['timestamp']):
                tick = {}
                tick['time'] = datetime.datetime.fromtimestamp(unixTimestamp)
                tick['open'] = data['chart']['result'][0]['indicators']['quote'][0]['open'][i]
                tick['close'] = data['chart']['result'][0]['indicators']['quote'][0]['close'][i]
                tick['low'] = data['chart']['result'][0]['indicators']['quote'][0]['low'][i]
                tick['high'] = data['chart']['result'][0]['indicators']['quote'][0]['high'][i]
                tick['volume'] = data['chart']['result'][0]['indicators']['quote'][0]['volume'][i]
                ticks.append(tick)

        return StockTicker(ticks)