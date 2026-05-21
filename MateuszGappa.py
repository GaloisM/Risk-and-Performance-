# %%

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb



# %% [markdown]
# ## Introduction to the Analysis
# 
# The project is divided into three main parts:
# 
# 1. **Data preparation and presentation**  
# 2. **Basic risk analysis**  
# 3. **Backtesting analysis**
# 
# Each section includes executable code that allows the reader to fully reproduce the results if they wish to follow the workflow step by step.

# %%
tickers = ["META","AAPL","TGT","EXPD","UNH","SBUX","ZBRA","MRNA","ACN","TSN"]

data = yf.download(
    tickers,
    start="2022-01-01",
    end="2025-01-01",
    auto_adjust=True,
    group_by="ticker"
)



# %%
Close_price = data.filter(like="Close")
Daily_returns = (Close_price - Close_price.shift(1))/Close_price.shift(1)


fig, axes = plt.subplots(5, 2, figsize=(6, 15))
axes = axes.flatten()

for ax, ticker in zip(axes, tickers):
    ax.hist(Daily_returns[ticker], color="blue", bins=50, edgecolor="black", zorder=2)
    ax.set_title(f"{ticker} returns")
    ax.set_xlabel("USD amount")
    ax.set_ylabel("quantity")
    ax.grid(zorder=1)
    
plt.tight_layout()
plt.show()




# %%
fig, axes = plt.subplots(5, 2, figsize=(10, 15))
axes = axes.flatten()

for ax, ticker in zip(axes, tickers):
    ax.plot(Daily_returns[ticker], linewidth=1.5, zorder=2)
    ax.set_title(f"{ticker} daily returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Return")
    ax.grid(zorder=1)

plt.tight_layout()
plt.show()

# %%
for ticker in tickers:
    plt.plot(Close_price[ticker])
    plt.title(f"{ticker} Price")
    plt.xlabel("Date")
    plt.xticks(rotation=45) 
    plt.ylabel("Price")
    plt.grid(zorder = 1)
    plt.show()

# %%
normalized_data = (Close_price / Close_price.iloc[0])*100
company_names = {
    "META": "Meta Platforms, Inc.",
    "AAPL": "Apple Inc.",
    "ACN": "Accenture plc",
    "MRNA": "Moderna, Inc.",
    "ZBRA": "Zebra Technologies",
    "SBUX": "Starbucks Corporation",
    "EXPD": "Expeditors International",
    "TGT": "Target Corporation",
    "UNH": "UnitedHealth Group",
    "TSN": "Tyson Foods"
}
normalized_data = normalized_data.rename(columns=company_names)

plt.figure(figsize=(15, 6))


normalized_data.plot(ax=plt.gca()) 

plt.title("Growth of Stock Prices")
plt.xlabel("Date")
plt.ylabel("Normalized Percentage Growth")
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)
plt.show()

# %%
Daily_returns_named = Daily_returns.rename(columns=company_names)

# %%

correlation_matrix = Daily_returns_named.corr()

correlation_matrix
plt.figure(figsize=(8,6))
sb.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()


# %%
stats = Daily_returns_named.agg(["mean", "var"]).T
stats = round(stats,5)
stats.index = stats.index.get_level_values(0)
print(stats)


# %%
Daily_returns_2022 = Daily_returns_named.loc["2022-01-01":"2022-12-31"].dropna()


# %%
Daily_returns_2022

# %%
companies = Daily_returns_2022.columns.get_level_values(0)


# %%

def max_drawdown(returns):



    equity = (1 + returns).cumprod()

    # running maximum
    running_max = equity.cummax()

    # drawdown series
    drawdown = equity / running_max - 1.0

    # maximum drawdown (most negative value)
    return drawdown.min()



# %%
mdd = {}

for company in companies:
    r = Daily_returns_2022[(company, "Close")].dropna()
    mdd[company] = max_drawdown(r)

mdd = pd.Series(mdd, name="Max Drawdown")
print(mdd)

# %%
companies = Daily_returns_2022.columns.get_level_values(0).unique()

sharpe = pd.Series({
    c: Daily_returns_2022[(c, "Close")].mean()
       / Daily_returns_2022[(c, "Close")].std()
    for c in companies
}, name= "Sharpe ratio")

sharpe * np.sqrt(252)
sr = round(sharpe,4)
print(sr)

# %%

mdd = pd.Series({
    c: max_drawdown(Daily_returns_2022[(c, "Close")])
    for c in companies
},name = "max_drawdown")
print(mdd*2000)

# %%

companies = Daily_returns_2022.columns.get_level_values(0).unique()

var_level = 0.01
es_level = 0.025

sharpe = pd.Series({
    c: Daily_returns_2022[(c, "Close")].mean()
       / Daily_returns_2022[(c, "Close")].std()
    for c in companies
}, name= "Sharpe ratio")

sharpe * np.sqrt(252)
sr = round(sharpe,4)

mdd = pd.Series({
    c: max_drawdown(Daily_returns_2022[(c, "Close")])
    for c in companies
},name = "max_drawdown")

mean_series = pd.Series({
    c: Daily_returns_2022[(c, "Close")].mean()
    for c in companies
}, name="Mean (daily)")

std_series = pd.Series({
    c: Daily_returns_2022[(c, "Close")].std(ddof=1)
    for c in companies
}, name="Std (daily)")

var_series = pd.Series({
    c: -Daily_returns_2022[(c, "Close")].quantile(var_level)
    for c in companies
}, name="VaR 1%")

es_series = pd.Series({
    c: -Daily_returns_2022[(c, "Close")]
        [Daily_returns_2022[(c, "Close")] 
         <= Daily_returns_2022[(c, "Close")].quantile(es_level)]
        .mean()
    for c in companies
}, name="ES 2.5%")


# %%
risk_basic_2022 = pd.concat(
    [mean_series, std_series, var_series, es_series,sr,mdd],
    axis=1
)

risk_basic_2022 = round(risk_basic_2022,4)

risk_basic_2022['Std (daily)'] = risk_basic_2022['Std (daily)']*2000
risk_basic_2022['VaR 1%'] = risk_basic_2022['VaR 1%']*2000
risk_basic_2022['ES 2.5%'] = risk_basic_2022['ES 2.5%']*2000
risk_basic_2022['max_drawdown'] = risk_basic_2022['max_drawdown']*2000
print(risk_basic_2022) 


# %%
Close_price_2 = data.loc["2022-01-01":"2022-12-31"].filter(like="Close")

# %%
normalized_data = (Close_price_2 / Close_price_2.iloc[0])*2000
company_names = {
    "META": "Meta Platforms, Inc.",
    "AAPL": "Apple Inc.",
    "ACN": "Accenture plc",
    "MRNA": "Moderna, Inc.",
    "ZBRA": "Zebra Technologies",
    "SBUX": "Starbucks Corporation",
    "EXPD": "Expeditors International",
    "TGT": "Target Corporation",
    "UNH": "UnitedHealth Group",
    "TSN": "Tyson Foods"
}
normalized_data = normalized_data.rename(columns=company_names)

plt.figure(figsize=(15, 6))


normalized_data.plot(ax=plt.gca()) 

plt.title("Growth of Stock Prices")
plt.xlabel("Date")
plt.ylabel("2000$ invested")
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)
plt.show()

# %%
selected_3 = [
    "UnitedHealth Group",
    "Starbucks Corporation",
    "Expeditors International",
]

# %%
selected_7 = [
    "Meta Platforms, Inc.","Apple Inc.","Accenture plc","Moderna, Inc.","Zebra Technologies","Target Corporation","Tyson Foods",
]

# %%
selected_5 = [
    "UnitedHealth Group",
    "Starbucks Corporation",
    "Expeditors International",
    "Apple Inc.",
    "Zebra Technologies",
]

# ES jako miara ryzyka
es = risk_basic_2022.loc[selected_5, "ES 2.5%"]

# wagi odwrotne do ES
weights = (1 / es)
weights = weights / weights.sum()

weights.rename("weight")
weights= round(weights,4)
weights

# %%


def portfolio_returns_from_assets(df, assets, weights=None):
    """
    df: DataFrame with MultiIndex columns (Company, "Close") containing SIMPLE returns
    assets: list of asset names
    weights: optional list/array of weights (will be normalized)
    """
    R = pd.DataFrame({a: df[(a, "Close")] for a in assets}).dropna()

    if weights is None:
        w = np.ones(len(assets)) / len(assets)  # equal weights
    else:
        w = np.array(weights, dtype=float)
        w = w / w.sum()

    return pd.Series(R.values @ w, index=R.index, name="Portfolio return")

def max_drawdown_from_simple_returns(ret: pd.Series) -> float:
    """
    Computes maximum drawdown from SIMPLE returns
    """
    equity = (1 + ret).cumprod()
    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    return float(drawdown.min())  # negative value

def portfolio_metrics(
    port_ret: pd.Series,
    var_level: float = 0.01,
    es_level: float = 0.025,
    rf_annual: float = 0.0,
    trading_days: int = 252
) -> pd.Series:
    """
    Empirical risk and performance metrics based on SIMPLE returns
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
    mdd = max_drawdown_from_simple_returns(port_ret)

    return pd.Series({
        "Mean (daily)": mean_d,
        "Std (daily)": std_d,
        "VaR 1%": var_val,
        "ES 2.5%": es_val,
        "Sharpe (ann.)": sharpe,
        "Max Drawdown": mdd
    })


# %%
top3 = [
    "UnitedHealth Group",
    "Starbucks Corporation",
    "Expeditors International"
]

port_top3 = portfolio_returns_from_assets(
    Daily_returns_2022,
    top3
)

metrics_top3 = portfolio_metrics(
    port_top3,
    rf_annual=0.03
)

metrics_top3

# %%
portfolio_comparison = pd.DataFrame({
    "Top-3 (equal)": metrics_top3,
    "Exclude-3 (equal)": metrics_excl,
    "Optimized-5 (inv ES)": metrics_opt
}).T

portfolio_comparison


# %%
opt5 = [
    "UnitedHealth Group",
    "Starbucks Corporation",
    "Expeditors International",
    "Apple Inc.",
    "Zebra Technologies"
]

# inverse ES weights
w_opt = 1 / risk_basic_2022.loc[opt5, "ES 2.5%"]
w_opt = w_opt / w_opt.sum()

port_opt = portfolio_returns_from_assets(
    Daily_returns_2022,
    opt5,
    weights=w_opt.values
)

metrics_opt = portfolio_metrics(
    port_opt,
    rf_annual=0.03
)

metrics_opt

# %%
all_companies = Daily_returns_2022.columns.get_level_values(0).unique()
exclude3 = [c for c in all_companies if c not in top3]

port_excl = portfolio_returns_from_assets(
    Daily_returns_2022,
    exclude3
)

metrics_excl = portfolio_metrics(
    port_excl,
    rf_annual=0.03
)

metrics_excl

# %%
comparison = pd.DataFrame({
    "Top-3 (equal)": metrics_top3,
    "Exclude-3 (equal)": metrics_excl,
    "Optimized-5 (inv ES)": metrics_opt
})


investment = 2000

comparison_usd = comparison.copy()
for row in ["Std (daily)", "VaR 1%", "ES 2.5%", "Max Drawdown"]:
    comparison_usd.loc[row] = comparison_usd.loc[row] * investment

print(comparison_usd.T)


# %%
def portfolio_value(returns: pd.Series, initial_capital: float = 2000) -> pd.Series:
    return initial_capital * (1 + returns).cumprod()


# %%
initial_capital = 2000

value_top3 = portfolio_value(port_top3, initial_capital).loc["2022-01-01":"2022-12-31"]
value_excl = portfolio_value(port_excl, initial_capital).loc["2022-01-01":"2022-12-31"]
value_opt  = portfolio_value(port_opt, initial_capital).loc["2022-01-01":"2022-12-31"]

portfolio_values = pd.DataFrame({
    "Top-3 (equal)": value_top3,
    "Exclude-3 (equal)": value_excl,
    "Optimized-5 (inv ES)": value_opt
})


# %%
plt.figure(figsize=(15, 6))

portfolio_values.plot(ax=plt.gca())

plt.title("Portfolio value evolution in 2022")
plt.xlabel("Date")
plt.ylabel("Portfolio value (USD)")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.2)

plt.show()

# %%
# Backtesting 
top3 = ["UNH", "SBUX", "EXPD"]

all_tickers = Daily_returns.columns.get_level_values(0).unique()
exclude3 = [t for t in all_tickers if t not in top3]

opt5 = ["UNH", "SBUX", "EXPD", "AAPL", "ZBRA"]


# %%
# round(w_opt,4)
weights = pd.Series({
    "UNH": 0.2853,
    "SBUX": 0.2017,
    "EXPD": 0.1918,
    "AAPL": 0.1963,
    "ZBRA": 0.1249
})
weights = weights / weights.sum()


# %%
def portfolio_returns_from_assets(df, tickers, weights=None):
    R = pd.DataFrame({t: df[(t, "Close")] for t in tickers}).dropna()

    if weights is None:
        w = np.ones(len(tickers)) / len(tickers)
    else:
        w = np.array(weights, dtype=float)
        w = w / w.sum()

    return pd.Series(R.values @ w, index=R.index, name="Portfolio return")


# %%
port_ret = portfolio_returns_from_assets(Daily_returns, opt5, weights=weights.loc[opt5].values)


# %%
lookback = 250
alpha = 0.01

VaR = -port_ret.rolling(lookback).quantile(alpha).shift(1)
VaR.name = "VaR_1pct"

bt = pd.concat([port_ret, VaR], axis=1).dropna()
bt = bt.loc["2023-01-01":"2024-12-31"]

bt["threshold"] = -bt["VaR_1pct"]
bt["exception"] = bt["Portfolio return"] < bt["threshold"]

N = len(bt)
E = int(bt["exception"].sum())
print(f"N={N}, Exceptions={E}, Expected={0.01*N:.2f}, Rate={E/N:.4f}")


# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 6))
bt["Portfolio return"].plot(ax=plt.gca(), label="Realised portfolio return")
bt["threshold"].plot(ax=plt.gca(), label="-VaR 1% (forecast)")

exc = bt[bt["exception"]]
plt.scatter(exc.index, exc["Portfolio return"], label="Exceptions", marker="o")

plt.title("VaR 1% Backtesting (2023–2024): Realised Returns vs Forecasted Risk Reserve")
plt.xlabel("Date")
plt.ylabel("Daily simple return")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.2)
plt.show()


# %%
port_equal = portfolio_returns_from_assets(
    Daily_returns,
    all_tickers  # brak wag → równe
)
lookback = 252
alpha = 0.01

VaR_eq = -port_equal.rolling(lookback).quantile(alpha).shift(1)
VaR_eq.name = "VaR_1pct"


bt_eq = pd.concat([port_equal, VaR_eq], axis=1).dropna()
bt_eq = bt_eq.loc["2023-01-01":"2024-12-31"]

bt_eq["threshold"] = -bt_eq["VaR_1pct"]
bt_eq["exception"] = bt_eq["Portfolio return"] < bt_eq["threshold"]

N_eq = len(bt_eq)
E_eq = int(bt_eq["exception"].sum())
expected_eq = 0.01 * N_eq

print(f"[Equal-weight portfolio]")
print(f"N = {N_eq}")
print(f"Observed exceptions = {E_eq}")
print(f"Expected exceptions = {expected_eq:.2f}")
print(f"Exception rate = {E_eq / N_eq:.4f}")

# %%
plt.figure(figsize=(15, 6))

bt_eq["Portfolio return"].plot(label="Realised portfolio return")
bt_eq["threshold"].plot(label="-VaR 1%")

exc_eq = bt_eq[bt_eq["exception"]]
plt.scatter(exc_eq.index, exc_eq["Portfolio return"], label="Exceptions", marker="o")

plt.title("VaR 1% Backtesting for Equal-Weight Portfolio (2023–2024)")
plt.xlabel("Date")
plt.ylabel("Daily simple return")
plt.legend()
plt.grid(alpha=0.2)
plt.show()


# %%


def portfolio_returns_from_assets(df, tickers, weights=None):
    R = pd.DataFrame({t: df[(t, "Close")] for t in tickers}).dropna()

    if weights is None:
        w = np.ones(len(tickers)) / len(tickers)
    else:
        w = np.array(weights, dtype=float)
        w = w / w.sum()

    return pd.Series(R.values @ w, index=R.index, name="Portfolio return")


# --- mapping ticker -> company name (bo risk_basic_2022 ma nazwy spółek) ---
ticker_to_company = {
    "ZBRA": "Zebra Technologies",
    "MRNA": "Moderna, Inc.",
    "META": "Meta Platforms, Inc.",
    "SBUX": "Starbucks Corporation",
    "ACN":  "Accenture plc",
    "EXPD": "Expeditors International",
    "UNH":  "UnitedHealth Group",
    "AAPL": "Apple Inc.",
    "TSN":  "Tyson Foods",
    "TGT":  "Target Corporation",
}

tickers_opt5 = ["UNH", "SBUX", "EXPD", "AAPL", "ZBRA"]
companies_opt5 = [ticker_to_company[t] for t in tickers_opt5]

# Equal-weight portfolio on the same 5 tickers
port_eq_5 = portfolio_returns_from_assets(Daily_returns, tickers_opt5)

# Optimized-5 weights: inverse ES (ES policzone w 2022)
w_opt = 1 / risk_basic_2022.loc[companies_opt5, "ES 2.5%"]
w_opt = w_opt / w_opt.sum()

port_opt5 = portfolio_returns_from_assets(Daily_returns, tickers_opt5, weights=w_opt.values)

# Evaluation period: 2024-01-01 to 2025-11-30
start, end = "2024-01-01", "2025-11-30"
r_eq = port_eq_5.loc[start:end].dropna()
r_opt = port_opt5.loc[start:end].dropna()


# %%


def realized_metrics(r: pd.Series, rf_annual=0.03, trading_days=252, bins_entropy=50, initial_capital=2000) -> pd.Series:
    mean_d = r.mean()
    var_d  = r.var(ddof=1)
    std_d  = r.std(ddof=1)

    rf_daily = rf_annual / trading_days
    sharpe_ann = np.nan if std_d == 0 else ((mean_d - rf_daily) / std_d) * np.sqrt(trading_days)

  

    # optional: realized wealth from $2000
    wealth = initial_capital * (1 + r).cumprod()
    final_wealth = float(wealth.iloc[-1])

    return pd.Series({
        "Mean (daily)": mean_d,
        
        "Std (daily)": std_d,
        "Sharpe (ann.)": sharpe_ann,
        
        "Final value (USD, $2000 start)": final_wealth
    })

summary_2425 = pd.DataFrame({
    "Equal-weight (5)": realized_metrics(r_eq),
    "Optimized-5 (inv ES)": realized_metrics(r_opt)
}).T

print(round(summary_2425,4))



