# Risk and Performance Measurement of Equity Portfolios

This repository contains a small portfolio analytics project focused on measuring both return performance and downside risk. The analysis compares a few simple equity portfolio construction rules and checks how well historical Value at Risk works on out-of-sample data.

The project was prepared for a risk and performance measurement course. It is intentionally built around transparent methods rather than a black-box optimization model, so each step can be inspected, reproduced, and discussed.

## What This Project Does

The notebook downloads daily stock prices, converts them into returns, builds several portfolios, and evaluates them with standard finance metrics. The main question is not only which portfolio earned the highest return, but whether that return was attractive after accounting for volatility, drawdowns, and tail risk.

The analysis covers:

- daily and annualized return,
- daily and annualized volatility,
- Sharpe ratio and Sortino ratio,
- maximum drawdown and Calmar ratio,
- historical Value at Risk (VaR),
- Expected Shortfall (ES / CVaR),
- rolling out-of-sample VaR backtesting.

## Portfolio Universe

The default stock universe is:

```text
META, AAPL, TGT, EXPD, UNH, SBUX, ZBRA, MRNA, ACN, TSN
```

Prices are downloaded from Yahoo Finance with `yfinance`. The current setup uses 2022 as the in-sample period and 2023-2024 as the out-of-sample testing period.

## Portfolio Strategies

The project compares three simple strategies:

| Strategy | Idea |
| --- | --- |
| Top 3 Equal Weight | Selects the three assets with the strongest in-sample average daily return and gives them equal weights. |
| Exclude Top 3 Equal Weight | Builds an equal-weight portfolio from the remaining assets after removing the top three performers. |
| Optimized 5 Inverse ES | Selects five strong assets and gives larger weights to assets with lower Expected Shortfall. |

These strategies are deliberately simple. The point is to make the risk-return trade-off visible instead of hiding it inside a complex optimizer.

## Repository Structure

```text
.
|-- notebooks/
|   `-- portfolio_analysis.ipynb   # main analysis notebook
|-- src/
|   |-- metrics.py                 # risk and performance metrics
|   `-- portfolio.py               # portfolio construction helpers
|-- PORTFOLIO_ANALYSIS.md          # methodology summary
|-- requirements.txt               # Python dependencies
|-- sourcing.ipynb                 # compatibility copy of the notebook
`-- README.md
```

If a LaTeX report is added later, the recommended location is:

```text
report/
|-- risk_performance_report.tex
|-- risk_performance_report.pdf
`-- figures/
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/GaloisM/Risk-and-Performance-.git
cd Risk-and-Performance-
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Open the notebook:

```bash
jupyter notebook notebooks/portfolio_analysis.ipynb
```

Then run the notebook cells from top to bottom.

## Methodology in Short

1. Download adjusted close prices for the selected stocks.
2. Calculate simple daily returns.
3. Use 2022 data to rank assets and construct portfolio weights.
4. Evaluate portfolio performance on 2023-2024 data.
5. Estimate 1% historical VaR with a 250-day rolling window.
6. Compare the realized exception rate with the expected 1% exception rate.

## Main Assumptions

- Portfolios are long-only.
- Transaction costs, taxes, bid-ask spreads, and slippage are ignored.
- Returns are simple daily returns, not log returns.
- VaR and ES are historical, empirical measures.
- Annualization uses 252 trading days.
- The project is educational and should not be treated as investment advice.

## Author

Mateusz Gappa
