import pandas as pd
import numpy as np


def compute_performance(df):

    mapping = {
        "SANADATE": (
            "SANADATE_PERF_W",
            "SANADATE_YTD"
        ),
        "BONDS": (
            "BONDS_PERF_W",
            "BONDS_YTD"
        ),
        "OBLIGATIONS": (
            "OBLIG_PERF_W",
            "OBLIG_YTD"
        )
    }

    result = []

    for fonds, cols in mapping.items():

        perf_col, ytd_col = cols

        r = pd.to_numeric(
            df[perf_col],
            errors="coerce"
        ).dropna()

        ytd = pd.to_numeric(
            df[ytd_col],
            errors="coerce"
        ).dropna()

        if len(r) == 0:
            continue

        # conversion si données en %
        if abs(r.mean()) > 1:
            r = r / 100

        perf_hebdo = r.iloc[-1]

        perf_ytd = ytd.iloc[-1]

        if abs(perf_ytd) > 1:
            perf_ytd = perf_ytd / 100

        volatilite = (
            r.std()
            * np.sqrt(52)
        )

        sharpe = 0

        if volatilite > 0:

            sharpe = (
                r.mean() * 52
            ) / volatilite

        result.append({

            "Fonds": fonds,

            "Perf Hebdo": perf_hebdo,

            "Perf YTD": perf_ytd,

            "Volatilité": volatilite,

            "Sharpe": sharpe

        })

    return pd.DataFrame(result)
