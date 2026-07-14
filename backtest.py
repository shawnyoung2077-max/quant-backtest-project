import yfinance as yf
import pandas as pd
import numpy as np

def calc_sharpe(data, short_window, long_window):
    d = data.copy()
    d["short_ma"] = d["Close"].rolling(short_window).mean()
    d["long_ma"] = d["Close"].rolling(long_window).mean()
    d["signal"] = (d["short_ma"] > d["long_ma"]).astype(int)
    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe

def walk_forward_validation(full_data, window_pairs, test_years):
    results = []
    for year in test_years:
        train_start = f"{year-3}-01-01"
        train_end = f"{year}-01-01"
        test_start = f"{year}-01-01"
        test_end = f"{year+1}-01-01"

        train_data = full_data.loc[train_start:train_end]
        test_data = full_data.loc[test_start:test_end]

        best_pair = None
        highest = -999

        for pair in window_pairs:
            train_sharpe = calc_sharpe(train_data, pair[0], pair[1])
            if train_sharpe > highest:
                highest = train_sharpe
                best_pair = pair

        test_sharpe = calc_sharpe(test_data, best_pair[0], best_pair[1])
        results.append((year, best_pair, highest, test_sharpe))

    return results

if __name__ == "__main__":
    full_data = yf.download("AAPL", start="2016-01-01", end="2024-01-01")
    full_data.columns = full_data.columns.droplevel(1)

    window_pairs = [(10, 30), (20, 50), (15, 45)]
    test_years = range(2019, 2024)

    results = walk_forward_validation(full_data, window_pairs, test_years)

    print("Year | Best Pair | Train Sharpe | Test Sharpe")
    print("-" * 50)
    for year, pair, train_sharpe, test_sharpe in results:
        print(f"{year} | {pair} | {train_sharpe:.3f} | {test_sharpe:.3f}")

    avg_test_sharpe = sum(r[3] for r in results) / len(results)
    print(f"\nAverage out-of-sample Sharpe: {avg_test_sharpe:.3f}")
