Project Status: MA Crossover Backtest — COMPLETE (Phase 1 + rigor extensions)
What's built, in order:

Basic backtest pipeline — Python script (backtest.py), pushed to GitHub. Pulls real AAPL data via yfinance, computes a 20/50-day MA crossover signal, calculates daily/cumulative returns, Sharpe ratio, and max drawdown.
Single train/test split — split 2016-2021 (train) vs 2022-2024 (test). Found (10,30) window pair generalized better than (20,50), despite (20,50) being marginally better on paper in training — first hands-on encounter with overfitting risk.
Multi-window comparison — tested (10,30), (20,50), (15,45), (30,100) on both periods; confirmed (10,30) was the more robust, non-fluky choice.
Walk-forward validation — built a 5-iteration rolling train(3yr)/test(1yr) loop, testing years 2019-2023. Key results:

Average out-of-sample Sharpe ≈ 1.19
(10,30) selected as best pair in 3 of 5 years — a repeated, non-coincidental pattern
Test Sharpe ranged from -0.57 to 2.58 — high year-to-year volatility, meaning the strategy's real-world reliability is inconsistent



Core honest finding (your actual research conclusion): A simple MA crossover strategy underperforms buy-and-hold overall, is structurally disadvantaged in strong trending bull markets (lagging indicator), and even after proper walk-forward validation shows unstable, inconsistent out-of-sample performance — a legitimate, well-supported conclusion, not a failed project.
Roadmap position: You've completed Phase 1 (working GitHub project) and are deep into Phase 2 rigor-building (robust validation methodology) — ahead of where the original plan expected you to be by this point in the summer.

