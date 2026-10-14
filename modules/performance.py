import pandas as pd
import numpy as np


def compute_performance(df):

    mapping = {
        "SANADATE": "SANADATE_VL",
        "BONDS": "BONDS_VL",
        "OBLIGATIONS": "OBLIG_VL"
    }

    result = []

    for nom, col in mapping.items():

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
            nav.iloc[-1] /
            nav.iloc[0]
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
                returns.mean()
                * 52
            ) / vol

        wealth = (
            1 + returns
        ).cumprod()

        drawdown = (
            wealth /
            wealth.cummax()
            - 1
        )

        result.append({

            "Fonds": nom,

            "Perf Cumulée": perf_cum,

            "Perf Annualisée": perf_ann,

            "Volatilité": vol,

            "Sharpe": sharpe,

            "Max Drawdown": drawdown.min()

        })

    return pd.DataFrame(result)
