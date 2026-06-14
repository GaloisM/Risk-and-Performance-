from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def clean_returns(returns: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Drop missing and infinite observations from return data."""
    cleaned = returns.replace([np.inf, -np.inf], np.nan)
    return cleaned.dropna()


def annualized_return(returns: pd.Series, periods_per_year: int = TRADING_DAYS) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    cumulative = (1 + returns).prod()
    years = len(returns) / periods_per_year
    return cumulative ** (1 / years) - 1


def annualized_volatility(returns: pd.Series, periods_per_year: int = TRADING_DAYS) -> float:
    returns = clean_returns(returns)
    return returns.std(ddof=1) * np.sqrt(periods_per_year)


def value_at_risk(returns: pd.Series, level: float = 0.01) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    return returns.quantile(level)


def expected_shortfall(returns: pd.Series, level: float = 0.025) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    var = value_at_risk(returns, level)
    tail = returns[returns <= var]
    return tail.mean() if not tail.empty else var


def max_drawdown(returns: pd.Series) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    wealth = (1 + returns).cumprod()
    running_max = wealth.cummax()
    drawdowns = wealth / running_max - 1
    return drawdowns.min()


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    excess_daily = returns - risk_free_rate / periods_per_year
    volatility = excess_daily.std(ddof=1)
    if volatility == 0 or np.isnan(volatility):
        return np.nan
    return excess_daily.mean() / volatility * np.sqrt(periods_per_year)


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    returns = clean_returns(returns)
    if returns.empty:
        return np.nan
    excess_daily = returns - risk_free_rate / periods_per_year
    downside = excess_daily[excess_daily < 0]
    downside_deviation = downside.std(ddof=1)
    if downside_deviation == 0 or np.isnan(downside_deviation):
        return np.nan
    return excess_daily.mean() / downside_deviation * np.sqrt(periods_per_year)


def calmar_ratio(returns: pd.Series, periods_per_year: int = TRADING_DAYS) -> float:
    mdd = abs(max_drawdown(returns))
    if mdd == 0 or np.isnan(mdd):
        return np.nan
    return annualized_return(returns, periods_per_year) / mdd


def performance_summary(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    var_level: float = 0.01,
    es_level: float = 0.025,
) -> dict[str, float]:
    returns = clean_returns(returns)
    return {
        "Mean Daily Return": returns.mean(),
        "Daily Volatility": returns.std(ddof=1),
        "Annualized Return": annualized_return(returns),
        "Annualized Volatility": annualized_volatility(returns),
        "VaR 1%": value_at_risk(returns, var_level),
        "ES 2.5%": expected_shortfall(returns, es_level),
        "Sharpe Ratio": sharpe_ratio(returns, risk_free_rate),
        "Sortino Ratio": sortino_ratio(returns, risk_free_rate),
        "Max Drawdown": max_drawdown(returns),
        "Calmar Ratio": calmar_ratio(returns),
    }


def summarize_assets(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.0,
    var_level: float = 0.01,
    es_level: float = 0.025,
) -> pd.DataFrame:
    rows = {
        column: performance_summary(
            returns[column],
            risk_free_rate=risk_free_rate,
            var_level=var_level,
            es_level=es_level,
        )
        for column in returns.columns
    }
    return pd.DataFrame(rows).T.sort_values("Sharpe Ratio", ascending=False)


def historical_var_backtest(
    returns: pd.Series,
    window: int = 250,
    level: float = 0.01,
) -> pd.DataFrame:
    returns = clean_returns(returns)
    if len(returns) <= window:
        raise ValueError("Backtest requires more observations than the rolling window.")

    rows = []
    for index in range(window, len(returns)):
        history = returns.iloc[index - window : index]
        realized = returns.iloc[index]
        var = value_at_risk(history, level)
        rows.append(
            {
                "Date": returns.index[index],
                "Realized Return": realized,
                "VaR": var,
                "Exception": realized < var,
            }
        )

    result = pd.DataFrame(rows).set_index("Date")
    result.attrs["expected_exception_rate"] = level
    result.attrs["actual_exception_rate"] = result["Exception"].mean()
    return result
