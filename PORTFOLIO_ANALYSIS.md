# Portfolio Risk Analysis and Backtesting

## Objective

The goal of this project is to measure and compare the risk-adjusted performance of selected equity portfolios. The analysis combines descriptive performance statistics with downside-risk measures and a simple historical VaR backtest.

## Data

The default universe contains ten US-listed stocks:

- META
- AAPL
- TGT
- EXPD
- UNH
- SBUX
- ZBRA
- MRNA
- ACN
- TSN

Daily adjusted close prices are downloaded with `yfinance` for the period from 2022-01-01 to 2025-01-01.

## Portfolio Construction

The notebook uses 2022 as an in-sample period and builds three strategies:

| Strategy | Description |
| --- | --- |
| Top 3 Equal Weight | Equal-weight allocation to the three assets with the highest average daily return in 2022. |
| Exclude Top 3 Equal Weight | Equal-weight allocation to all assets except the top three performers from 2022. |
| Optimized 5 Inverse ES | Allocation to five assets with the best Sharpe ratios, weighted inversely to Expected Shortfall. |

## Metrics

The project reports:

- mean daily return
- daily volatility
- annualized return
- annualized volatility
- 1% historical VaR
- 2.5% Expected Shortfall
- Sharpe ratio
- Sortino ratio
- maximum drawdown
- Calmar ratio

## Backtesting

The VaR backtest uses a 250-trading-day rolling historical window. For each out-of-sample day, the model estimates 1% historical VaR from the previous 250 daily returns and checks whether the realized return falls below that VaR threshold.

The expected exception rate is 1%. A much higher realized exception rate indicates that the model understated downside risk during the tested period.

## Main Limitations

- No transaction costs, bid-ask spreads, taxes, or market-impact assumptions.
- Portfolios are long-only and relatively simple.
- Historical VaR assumes the recent empirical distribution is informative for future risk.
- The framework is educational and should not be treated as investment advice.
