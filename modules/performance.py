import pandas as pd
import numpy as np


def compute_performance(df):

    fonds = {
        "SANADATE": "SANADATE_PERF_W",
        "BONDS": "BONDS_PERF_W",
        "OBLIGATIONS": "OBLIG_PERF_W"
    }

    lignes = []

    for nom, col in fonds.items():

        if col not in df.columns:
            continue

        r = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        # conversion %
        if r.abs().mean() > 0.10:
            r = r / 100

        perf_cum = (1 + r).prod() - 1

        perf_ann = (
            (1 + perf_cum)
            ** (52 / len(r))
            - 1
        )

        vol = r.std() * np.sqrt(52)

        sharpe = 0

        if vol != 0:
            sharpe = (
                r.mean() * 52
            ) / vol

        wealth = (1 + r).cumprod()

        drawdown = (
            wealth /
            wealth.cummax()
            - 1
        )

        lignes.append({

            "Fonds": nom,

            "Perf Cumulée": perf_cum,

            "Perf Annualisée": perf_ann,

            "Volatilité": vol,

            "Sharpe": sharpe,

            "Max Drawdown": drawdown.min()

        })

    return pd.DataFrame(lignes)
