import pandas as pd
import numpy as np


def compute_performance(df):

    mapping = {
        "SANADATE": "SANADATE_VL",
        "BONDS": "BONDS_VL",
        "OBLIGATIONS": "OBLIG_VL"
    }

    result = []

    for fonds, col in mapping.items():

        if col not in df.columns:
            continue

        nav = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        if len(nav) < 2:
            continue

        returns = nav.pct_change().dropna()

        perf_cum = (
            nav.iloc[-1]
            / nav.iloc[0]
            - 1
        )

        perf_ann = (
            (1 + perf_cum)
            ** (52 / len(returns))
            - 1
        )

        vol = (
            returns.std()
            * np.sqrt(52)
        )

        sharpe = 0

        if vol > 0:
            sharpe = (
                returns.mean() * 52
            ) / vol

        wealth = (
            1 + returns
        ).cumprod()

        drawdown = (
            wealth /
            wealth.cummax()
            - 1
        )

        max_dd = drawdown.min()

        calmar = 0

        if max_dd != 0:
            calmar = perf_ann / abs(max_dd)

        downside = returns[
            returns < 0
        ]

        sortino = 0

        if len(downside) > 0:

            downside_vol = (
                downside.std()
                * np.sqrt(52)
            )

            if downside_vol > 0:
                sortino = (
                    returns.mean() * 52
                ) / downside_vol

        result.append({

            "Fonds": fonds,

            "Perf Cumulée": perf_cum,

            "Perf Annualisée": perf_ann,

            "Volatilité": vol,

            "Sharpe": sharpe,

            "Sortino": sortino,

            "Max Drawdown": max_dd,

            "Calmar": calmar

        })

    return pd.DataFrame(result)
