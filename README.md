# Moving Average Crossover Backtest

A simple backtesting framework for a 20-day/50-day moving average crossover strategy on AAPL, built in Python with pandas.

## Strategy Logic
- Buy signal (1): 20-day moving average > 50-day moving average
- Sell/cash signal (0): 20-day moving average < 50-day moving average
- Returns are calculated using the *previous day's* signal to avoid lookahead bias.

## How to Run
pip install -r requirements.txt
python backtest.py
## Results (AAPL, 2016–2024)
- Market cumulative return: 6.26x
- Strategy cumulative return: 3.10x
- Market Sharpe ratio: 1.17
- Strategy Sharpe ratio: 1.00
- Strategy max drawdown: -22.6%

## Interpretation
The strategy underperformed buy-and-hold over this period. This is an expected result: AAPL experienced a strong, sustained bull run over 2016–2024, and moving average crossover strategies are lagging indicators — they enter trends late and exit on temporary dips, which costs performance in strongly trending markets. This strategy would be expected to perform relatively better in sideways or choppier markets, which is a direction for further testing.

## Next Steps
- Test performance across different time windows (e.g., sideways/bear markets)
- Add transaction cost modeling
- Extend to multi-factor signals with out-of-sample validation