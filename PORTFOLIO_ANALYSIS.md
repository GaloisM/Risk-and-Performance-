# Portfolio Risk Analysis & Backtesting
cd
## Overview

This project implements a comprehensive portfolio risk analysis framework including:
- **Risk Metrics Calculation** - VaR, ES, Sharpe ratio, maximum drawdown
- **Portfolio Construction** - Equal-weight and optimized (inverse ES) strategies
- **Backtesting** - Validation of risk models on out-of-sample data (2023-2024)
- **Performance Comparison** - Realized metrics for different portfolio strategies

## Project Structure

```
.
├── notebooks/
│   └── portfolio_analysis.ipynb      # Main analysis notebook
├── src/
│   ├── __init__.py
│   ├── metrics.py                    # Risk metrics calculations
│   └── portfolio.py                  # Portfolio construction
├── data/                              # Data directory (if needed)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Installation

1. **Create virtual environment** (if not already done):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis

Launch Jupyter notebook:
```bash
jupyter notebook notebooks/portfolio_analysis.ipynb
```

### Using the Library

```python
from src.metrics import portfolio_metrics, max_drawdown
from src.portfolio import portfolio_returns_from_assets, optimize_weights_inverse_es

# Calculate portfolio returns
port_returns = portfolio_returns_from_assets(data, assets=['AAPL', 'MSFT'])

# Calculate metrics
metrics = portfolio_metrics(port_returns, rf_annual=0.03)
print(metrics)

# Optimize weights based on inverse ES
weights = optimize_weights_inverse_es(risk_df, assets=['AAPL', 'MSFT'])
```

## Analysis Sections

### 1. Data Preparation
- Download historical price data for 10 stocks (2022-2025)
- Calculate daily returns
- Visualize price movements and correlations

### 2. Risk Analysis (2022)
- Calculate individual stock risk metrics
- Compare three portfolio strategies:
  - **Top-3 Equal Weight**: Equal allocation to 3 best performers
  - **Exclude-3 Equal Weight**: Equal allocation excluding top 3
  - **Optimized-5 (Inverse ES)**: Weighted by inverse Expected Shortfall
- Visualize portfolio value evolution

### 3. Backtesting (2023-2024)
- Validate VaR models using rolling 250-day windows
- Test both optimized and equal-weight portfolios
- Measure exception rates vs. theoretical expectations

## Key Metrics

- **Mean (daily)**: Average daily return
- **Std (daily)**: Daily standard deviation
- **VaR 1%**: Value at Risk at 99% confidence level
- **ES 2.5%**: Expected Shortfall (CVaR) at 97.5% confidence
- **Sharpe (ann.)**: Annualized Sharpe ratio
- **Max Drawdown**: Maximum loss from peak

## Assumptions & Limitations

- No transaction costs or slippage
- Simple (non-log) returns used throughout
- Historical VaR/ES based on empirical quantiles
- Risk-free rate assumed constant
- Weights rebalanced annually (2022 → 2023+)

## Data Sources

- Stock prices: Yahoo Finance via `yfinance`
- Period: 2022-01-01 to 2025-01-01
- Tickers: META, AAPL, TGT, EXPD, UNH, SBUX, ZBRA, MRNA, ACN, TSN

## Future Enhancements

- [ ] Transaction cost modeling
- [ ] Dynamic weight rebalancing
- [ ] GARCH volatility modeling
- [ ] Parametric VaR calculation
- [ ] Monte Carlo simulations
- [ ] Correlation stress testing

## Author

Mateusz Gappa

## License

MIT
