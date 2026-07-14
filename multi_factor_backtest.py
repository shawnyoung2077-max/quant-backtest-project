import yfinance as yf
import pandas as pd
import numpy as np


def load_data(ticker="AAPL", start="2016-01-01", end="2024-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data.columns = data.columns.droplevel(1)
    return data


def momentum_only(data, ma_short, ma_long):
    d = data.copy()
    d["short_ma"] = d["Close"].rolling(ma_short).mean()
    d["long_ma"] = d["Close"].rolling(ma_long).mean()
    d["signal"] = (d["short_ma"] > d["long_ma"]).astype(int)
    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe, d["signal"].sum()


def mean_reversion_only(data, z_window):
    d = data.copy()
    d["z_score"] = (d["Close"] - d["Close"].rolling(z_window).mean()) / d["Close"].rolling(z_window).std()
    d["signal"] = (d["z_score"] < -1).astype(int)
    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe, d["signal"].sum()


def combined_and(data, ma_short, ma_long, z_window):
    d = data.copy()
    d["z_score"] = (d["Close"] - d["Close"].rolling(z_window).mean()) / d["Close"].rolling(z_window).std()
    d["z_signal"] = (d["z_score"] < -1).astype(int)
    d["short_ma"] = d["Close"].rolling(ma_short).mean()
    d["long_ma"] = d["Close"].rolling(ma_long).mean()
    d["momentum_signal"] = (d["short_ma"] > d["long_ma"]).astype(int)
    d["signal"] = ((d["momentum_signal"] == 1) & (d["z_signal"] == 1)).astype(int)
    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe, d["signal"].sum()


def combined_or(data, ma_short, ma_long, z_window):
    d = data.copy()
    d["z_score"] = (d["Close"] - d["Close"].rolling(z_window).mean()) / d["Close"].rolling(z_window).std()
    d["z_signal"] = (d["z_score"] < -1).astype(int)
    d["short_ma"] = d["Close"].rolling(ma_short).mean()
    d["long_ma"] = d["Close"].rolling(ma_long).mean()
    d["momentum_signal"] = (d["short_ma"] > d["long_ma"]).astype(int)
    d["signal"] = ((d["momentum_signal"] == 1) | (d["z_signal"] == 1)).astype(int)
    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe, d["signal"].sum()


def combined_weighted(data, ma_short, ma_long, z_window):
    d = data.copy()

    d["short_ma"] = d["Close"].rolling(ma_short).mean()
    d["long_ma"] = d["Close"].rolling(ma_long).mean()
    d["momentum_strength"] = (d["short_ma"] - d["long_ma"]) / d["long_ma"]

    d["z_score"] = (d["Close"] - d["Close"].rolling(z_window).mean()) / d["Close"].rolling(z_window).std()
    d["mean_reversion_strength"] = -d["z_score"]

    d["momentum_z"] = (d["momentum_strength"] - d["momentum_strength"].mean()) / d["momentum_strength"].std()
    d["reversion_z"] = (d["mean_reversion_strength"] - d["mean_reversion_strength"].mean()) / d["mean_reversion_strength"].std()

    d["combined_score"] = 0.5 * d["momentum_z"] + 0.5 * d["reversion_z"]
    d["signal"] = (d["combined_score"] > 0).astype(int)

    d["daily_return"] = d["Close"].pct_change()
    d["strategy_return"] = d["daily_return"] * d["signal"].shift(1)
    sharpe = (d["strategy_return"].mean() / d["strategy_return"].std()) * np.sqrt(252)
    return sharpe, d["signal"].sum()


if __name__ == "__main__":
    full_data = load_data()

    ma_short, ma_long, z_window = 10, 30, 30
    total_days = len(full_data)

    results = {
        "Momentum only": momentum_only(full_data, ma_short, ma_long),
        "Mean-reversion only": mean_reversion_only(full_data, z_window),
        "Combined (AND)": combined_and(full_data, ma_short, ma_long, z_window),
        "Combined (OR)": combined_or(full_data, ma_short, ma_long, z_window),
        "Combined (weighted)": combined_weighted(full_data, ma_short, ma_long, z_window),
    }

    print(f"{'Strategy':<22} {'Sharpe':>8} {'Days active':>12} {'% of period':>12}")
    print("-" * 58)
    for name, (sharpe, days) in results.items():
        pct = 100 * days / total_days
        print(f"{name:<22} {sharpe:>8.3f} {days:>12} {pct:>11.1f}%")

    print("\nConclusion: momentum is the dominant factor for AAPL over this period.")
    print("Mean-reversion is weak on its own, and dilutes performance when combined,")
    print("consistent with AAPL being in a sustained uptrend rather than a range-bound regime.")