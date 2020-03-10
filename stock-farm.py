
import sys, getopt

from modules.simulation import StrategySimulator
from modules.simulation import MarketSimulator
from modules.strategies.default import DefaultStrategy
from modules.investments import Portfolio

def main(argv):
    """
    StockFarm entry point.

    """
    
    # default argument values
    marketSymbol = None
    strategyName = "default"

    # parse command line arguments
    try:
        opts, args = getopt.getopt(argv,"hm:s:",["market=","strategy="])
    except getopt.GetoptError:
        print('stock-farm.py -m <market symbol> -s <strategy name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('stock-farm.py -m <market symbol> -s <strategy name>')
            sys.exit()
        if opt in ('-m', '--market'):
            marketSymbol = arg
        elif opt in ('-s', '--strategy'):
            strategyName = arg

    if marketSymbol == None:
        print('Missing input parameter: -m, --market')
        sys.exit(2)

    portfolio = Portfolio(1000)
    strategy = DefaultStrategy()
    marketSimulator = MarketSimulator(marketSymbol)
    simulator = StrategySimulator(marketSimulator, strategy, portfolio)
    simulator.run()
    print(portfolio.getValue())

if __name__ == "__main__":
	main(sys.argv[1:])