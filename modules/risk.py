import numpy as np

def var_historique(series, alpha=0.05):

    return np.quantile(series, alpha)

def cvar(series, alpha=0.05):

    var = np.quantile(series, alpha)

    return series[series <= var].mean()

def max_drawdown(values):

    peak = values.cummax()

    drawdown = values / peak - 1

    return drawdown.min()

def compute_risk_metrics(perf_df, sensi_df):

    return {}
