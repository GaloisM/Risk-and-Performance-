from __future__ import annotations

import numpy as np
import pandas as pd

from .metrics import expected_shortfall


def normalize_weights(weights: pd.Series | dict[str, float]) -> pd.Series:
    weights = pd.Series(weights, dtype=float)
    if (weights < 0).any():
        raise ValueError("This project expects long-only weights.")
    total = weights.sum()
    if total <= 0 or np.isnan(total):
        raise ValueError("Weights must sum to a positive value.")
    return weights / total


def equal_weights(assets: list[str]) -> pd.Series:
    if not assets:
        raise ValueError("At least one asset is required.")
    return pd.Series(1 / len(assets), index=assets, name="Weight")


def portfolio_returns(returns: pd.DataFrame, weights: pd.Series | dict[str, float]) -> pd.Series:
    weights = normalize_weights(weights)
    missing = sorted(set(weights.index) - set(returns.columns))
    if missing:
        raise KeyError(f"Missing return columns for assets: {missing}")
    aligned_returns = returns.loc[:, weights.index].dropna()
    result = aligned_returns.dot(weights)
    result.name = "Portfolio Return"
    return result


def top_assets_by_return(returns: pd.DataFrame, n: int = 3) -> list[str]:
    if n <= 0:
        raise ValueError("n must be positive.")
    return returns.mean().sort_values(ascending=False).head(n).index.tolist()


def inverse_expected_shortfall_weights(
    returns: pd.DataFrame,
    assets: list[str],
    level: float = 0.025,
) -> pd.Series:
    if not assets:
        raise ValueError("At least one asset is required.")

    es_values = returns[assets].apply(lambda series: abs(expected_shortfall(series, level)))
    es_values = es_values.replace(0, np.nan).dropna()
    if es_values.empty:
        return equal_weights(assets)

    inverse_risk = 1 / es_values
    weights = normalize_weights(inverse_risk)
    return weights.reindex(assets).fillna(0).rename("Weight")


def build_strategy_returns(
    returns: pd.DataFrame,
    strategy_weights: dict[str, pd.Series],
) -> pd.DataFrame:
    portfolios = {
        name: portfolio_returns(returns, weights)
        for name, weights in strategy_weights.items()
    }
    return pd.DataFrame(portfolios).dropna()
