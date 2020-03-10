
import sys
import json
import datetime

from pathlib import Path

class YahooFinanceParser:
    '''
    This class parses historic stock data from Yahoo Finance.

    '''

    def __init__(self, symbol):
        self.symbol = symbol
        self.parseJson()
        print(self.data)

    def parseJson(self):
        """
		Read the json file of the configured stock market

		"""
        dataFilePath = Path('data/' + self.symbol + '.json')

        if not dataFilePath.is_file():
            print('File ' + str(dataFilePath) + ' not found!')
            sys.exit(2)

        self.data = []
        with open(dataFilePath) as dataFile:
            data = json.load(dataFile)

            for i, unixTimestamp in enumerate(data['chart']['result'][0]['timestamp']):
                moment = {}
                moment['time'] = datetime.datetime.fromtimestamp(unixTimestamp)
                moment['open'] = data['chart']['result'][0]['indicators']['quote'][0]['open'][i]
                moment['close'] = data['chart']['result'][0]['indicators']['quote'][0]['close'][i]
                moment['low'] = data['chart']['result'][0]['indicators']['quote'][0]['low'][i]
                moment['high'] = data['chart']['result'][0]['indicators']['quote'][0]['high'][i]
                moment['volume'] = data['chart']['result'][0]['indicators']['quote'][0]['volume'][i]