import yfinance as yf
import pandas as pd
import numpy as np

def run_backtest(ticker="AAPL", start="2016-07-12", end="2024-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data.columns = data.columns.droplevel(1)

    data["20-day moving average"] = data["Close"].rolling(window=20).mean()
    data["50-day moving average"] = data["Close"].rolling(window=50).mean()
    data["signal"] = (data["20-day moving average"] > data["50-day moving average"]).astype(int)
    data["daily_return"] = data["Close"].pct_change()
    data["strategy_return"] = data["daily_return"] * data["signal"].shift(1)
    data["cumulative_market_return"] = (1 + data["daily_return"]).cumprod()
    data["cumulative_strategy_return"] = (1 + data["strategy_return"]).cumprod()

    market_sharpe = (data["daily_return"].mean() / data["daily_return"].std()) * np.sqrt(252)
    strategy_sharpe = (data["strategy_return"].mean() / data["strategy_return"].std()) * np.sqrt(252)

    running_max = data["cumulative_strategy_return"].cummax()
    drawdown = (data["cumulative_strategy_return"] - running_max) / running_max

    print("Final Performance Summary")
    print("--------------------------")
    print("Market cumulative return:", data["cumulative_market_return"].iloc[-1])
    print("Strategy cumulative return:", data["cumulative_strategy_return"].iloc[-1])
    print("Market Sharpe ratio:", market_sharpe)
    print("Strategy Sharpe ratio:", strategy_sharpe)
    print("Strategy max drawdown:", drawdown.min())

    return data

if __name__ == "__main__":
    run_backtest()