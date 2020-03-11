# Stock-Farm
Framework for testing investment strategies on historic data

## Usage
Create a strategy by extending the `Strategy` class from `modules.strategies.strategy`.

Run the strategy simulation for the desired market and strategy:
```
$ stock-farm.py -m <market symbol> -s <strategy name>
```