"""
Portfolio risk and performance metrics calculation module.
"""
import numpy as np
import pandas as pd


def max_drawdown(returns: pd.Series) -> float:
    """
    Calculate maximum drawdown from simple returns.
    
    Parameters:
    -----------
    returns : pd.Series
        Series of simple returns
    
    Returns:
    --------
    float
        Maximum drawdown (negative value)
    """
    equity = (1 + returns).cumprod()
    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    return float(drawdown.min())


def portfolio_metrics(
    port_ret: pd.Series,
    var_level: float = 0.01,
    es_level: float = 0.025,
    rf_annual: float = 0.0,
    trading_days: int = 252
) -> pd.Series:
    """
    Calculate empirical risk and performance metrics based on simple returns.
    
    Parameters:
    -----------
    port_ret : pd.Series
        Portfolio simple returns time series
    var_level : float
        VaR confidence level (default 0.01 = 99%)
    es_level : float
        ES confidence level (default 0.025 = 97.5%)
    rf_annual : float
        Annual risk-free rate (default 0.0)
    trading_days : int
        Trading days per year (default 252)
    
    Returns:
    --------
    pd.Series
        Series containing:
        - Mean (daily): Daily mean return
        - Std (daily): Daily standard deviation
        - VaR 1%: Value at Risk at specified level
        - ES 2.5%: Expected Shortfall at specified level
        - Sharpe (ann.): Annualized Sharpe ratio
        - Max Drawdown: Maximum drawdown
    """
    mean_d = port_ret.mean()
    std_d = port_ret.std(ddof=1)
    
    # Historical VaR and ES
    var_val = -port_ret.quantile(var_level)
    es_val = -port_ret[port_ret <= port_ret.quantile(es_level)].mean()
    
    # Annualized Sharpe ratio
    rf_daily = rf_annual / trading_days
    sharpe = np.nan
    if std_d > 0:
        sharpe = ((mean_d - rf_daily) / std_d) * np.sqrt(trading_days)
    
    # Maximum drawdown
    mdd = max_drawdown(port_ret)
    
    return pd.Series({
        "Mean (daily)": mean_d,
        "Std (daily)": std_d,
        "VaR 1%": var_val,
        "ES 2.5%": es_val,
        "Sharpe (ann.)": sharpe,
        "Max Drawdown": mdd
    })


def realized_metrics(
    r: pd.Series,
    rf_annual: float = 0.03,
    trading_days: int = 252,
    initial_capital: float = 2000
) -> pd.Series:
    """
    Calculate realized performance metrics.
    
    Parameters:
    -----------
    r : pd.Series
        Simple returns time series
    rf_annual : float
        Annual risk-free rate (default 0.03)
    trading_days : int
        Trading days per year (default 252)
    initial_capital : float
        Starting investment amount (default 2000)
    
    Returns:
    --------
    pd.Series
        Series containing realized metrics and final wealth
    """
    mean_d = r.mean()
    std_d = r.std(ddof=1)
    
    rf_daily = rf_annual / trading_days
    sharpe_ann = np.nan if std_d == 0 else ((mean_d - rf_daily) / std_d) * np.sqrt(trading_days)
    
    wealth = initial_capital * (1 + r).cumprod()
    final_wealth = float(wealth.iloc[-1])
    
    return pd.Series({
        "Mean (daily)": mean_d,
        "Std (daily)": std_d,
        "Sharpe (ann.)": sharpe_ann,
        "Final value (USD, $2000 start)": final_wealth
    })
