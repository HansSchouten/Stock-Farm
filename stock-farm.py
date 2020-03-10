
import sys, getopt

from modules.simulation import StrategySimulator
from modules.simulation import MarketSimulator
from modules.strategies.strategy import NothingStrategy
from modules.strategies.trends import SimpleTrendStrategy
from modules.portfolio import Portfolio

def main(argv):
    """
    StockFarm entry point.

    """
    
    # default argument values
    marketSymbol = None
    strategyName = "nothing"

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

    # ensure all required arguments have been passed
    if marketSymbol == None:
        print('Missing input parameter: -m, --market')
        sys.exit(2)
        
    strategy = NothingStrategy()
    if strategyName == 'simple-trends':
        strategy = SimpleTrendStrategy()

    portfolio = Portfolio(1000)
    marketSimulator = MarketSimulator(marketSymbol)
    strategySimulator = StrategySimulator(marketSimulator, strategy, portfolio)
    
    print("Initial portfolio value: " + str(portfolio.getValue()))
    strategySimulator.run()
    print("Portfolio value after strategy simulation: " + str(portfolio.getValue()))

if __name__ == "__main__":
	main(sys.argv[1:])