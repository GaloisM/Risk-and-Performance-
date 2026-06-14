# Portfolio Risk and Performance Measurement

This project analyzes a multi-asset equity portfolio using common risk and performance measures:

- historical Value at Risk (VaR)
- Expected Shortfall (ES / CVaR)
- annualized return and volatility
- Sharpe and Sortino ratios
- maximum drawdown and Calmar ratio
- simple out-of-sample VaR backtesting

The analysis is written as a reproducible Jupyter notebook and supported by small Python modules in `src/`.

## Repository Structure

```text
.
|-- notebooks/
|   `-- portfolio_analysis.ipynb
|-- src/
|   |-- __init__.py
|   |-- metrics.py
|   `-- portfolio.py
|-- PORTFOLIO_ANALYSIS.md
|-- README.md
|-- requirements.txt
`-- sourcing.ipynb
```

`sourcing.ipynb` is kept as a compatibility placeholder. The main work is in `notebooks/portfolio_analysis.ipynb`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Analysis

```bash
jupyter notebook notebooks/portfolio_analysis.ipynb
```

The notebook downloads adjusted close prices from Yahoo Finance using `yfinance`.

Default universe:

```text
META, AAPL, TGT, EXPD, UNH, SBUX, ZBRA, MRNA, ACN, TSN
```

## Methodology

1. Download daily adjusted close prices.
2. Convert prices to simple daily returns.
3. Use 2022 as the in-sample period for ranking and portfolio construction.
4. Compare three portfolio strategies:
   - Top 3 equal weight
   - Excluding top 3 equal weight
   - Optimized 5 using inverse Expected Shortfall weights
5. Backtest 1% historical VaR on 2023-2024 out-of-sample returns.

## Assumptions

- Long-only portfolios.
- No transaction costs, taxes, or slippage.
- Simple daily returns are used instead of log returns.
- Historical VaR and ES are based on empirical quantiles.
- Annualization assumes 252 trading days.

## Author

Mateusz Gappa
