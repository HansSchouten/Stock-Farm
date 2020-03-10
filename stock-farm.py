import sys, getopt

from modules.simulator import StrategySimulator
from modules.simulator import MarketSimulator
from modules.strategies.default import DefaultStrategy

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

    strategy = DefaultStrategy()
    market = MarketSimulator(strategyName)
    simulation = StrategySimulator(market, strategy)

if __name__ == "__main__":
	main(sys.argv[1:])