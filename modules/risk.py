import pandas as pd
import numpy as np


def max_drawdown(nav):

    drawdown = nav / nav.cummax() - 1

    return drawdown.min()


def compute_risk_metrics(perf_df, sensi_df):

    result = []

    mapping = {
        "SANADATE": "SANADATE_VL",
        "BONDS": "BONDS_VL",
        "OBLIGATIONS": "OBLIG_VL"
    }

    for nom, col in mapping.items():

        if col not in perf_df.columns:
            continue

        nav = perf_df[col].dropna()

        if len(nav) < 2:
            continue

        r = nav.pct_change().dropna()

        var95 = np.percentile(r, 5)
        var99 = np.percentile(r, 1)

        cvar95 = r[r <= var95].mean()
        cvar99 = r[r <= var99].mean()

        vol_ann = r.std() * np.sqrt(52)

        mdd = max_drawdown(nav)

        result.append(
            {
                "Fonds": nom,
                "Volatilité": vol_ann,
                "VaR95": var95,
                "VaR99": var99,
                "CVaR95": cvar95,
                "CVaR99": cvar99,
                "Max Drawdown": mdd,
                "Worst Week": r.min(),
                "Best Week": r.max(),
                "Skewness": r.skew(),
                "Kurtosis": r.kurt()
            }
        )

    return pd.DataFrame(result)
