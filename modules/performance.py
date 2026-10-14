import pandas as pd
import numpy as np


def sharpe_ratio(r):

    vol = r.std()

    if vol == 0:
        return 0

    return r.mean() / vol


def sortino_ratio(r):

    downside = r[r < 0]

    if len(downside) == 0:
        return 0

    downside_std = downside.std()

    if downside_std == 0:
        return 0

    return r.mean() / downside_std


def annualized_return(r):

    if len(r) == 0:
        return 0

    return ((1 + r).prod()) ** (52 / len(r)) - 1


def compute_performance(df):

    fonds = {
        "SANADATE": "SANADATE_VL",
        "BONDS": "BONDS_VL",
        "OBLIGATIONS": "OBLIG_VL"
    }

    result = []

    for nom, col in fonds.items():

        if col not in df.columns:
            continue

        nav = df[col].dropna()

        if len(nav) < 2:
            continue

        r = nav.pct_change().dropna()

        perf_ann = annualized_return(r)

        vol = r.std() * np.sqrt(52)

        sharpe = sharpe_ratio(r)

        sortino = sortino_ratio(r)

        perf_total = nav.iloc[-1] / nav.iloc[0] - 1

        mdd = (nav / nav.cummax() - 1).min()

        calmar = 0

        if abs(mdd) > 0:
            calmar = perf_ann / abs(mdd)

        result.append({
            "Fonds": nom,
            "Perf Cumulée": perf_total,
            "Perf Annualisée": perf_ann,
            "Volatilité": vol,
            "Sharpe": sharpe,
            "Sortino": sortino,
            "Max Drawdown": mdd,
            "Calmar": calmar
        })

    return pd.DataFrame(result)
