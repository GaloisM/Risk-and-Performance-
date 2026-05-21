"""
Portfolio construction and return calculation module.
"""
import numpy as np
import pandas as pd


def portfolio_returns_from_assets(
    df: pd.DataFrame,
    assets: list,
    weights: np.ndarray = None
) -> pd.Series:
    """
    Calculate portfolio returns from individual asset returns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with MultiIndex columns (Asset, "Close") or regular columns
    assets : list
        List of asset names to include in portfolio
    weights : np.ndarray, optional
        Portfolio weights. If None, equal weights are used.
    
    Returns:
    --------
    pd.Series
        Portfolio simple returns time series
    """
    # Handle MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        R = pd.DataFrame({a: df[(a, "Close")] for a in assets}).dropna()
    else:
        R = pd.DataFrame({a: df[a] for a in assets}).dropna()
    
    if weights is None:
        w = np.ones(len(assets)) / len(assets)
    else:
        w = np.array(weights, dtype=float)
        w = w / w.sum()
    
    return pd.Series(R.values @ w, index=R.index, name="Portfolio return")


def optimize_weights_inverse_es(
    risk_metrics: pd.DataFrame,
    assets: list,
    risk_column: str = "ES 2.5%"
) -> pd.Series:
    """
    Calculate portfolio weights based on inverse risk metric.
    
    Parameters:
    -----------
    risk_metrics : pd.DataFrame
        DataFrame with risk metrics (rows: assets, columns: metrics)
    assets : list
        List of asset names to optimize
    risk_column : str
        Column name for risk metric to invert (default "ES 2.5%")
    
    Returns:
    --------
    pd.Series
        Normalized portfolio weights
    """
    es_selected = risk_metrics.loc[assets, risk_column]
    weights = 1 / es_selected
    weights = weights / weights.sum()
    return weights
