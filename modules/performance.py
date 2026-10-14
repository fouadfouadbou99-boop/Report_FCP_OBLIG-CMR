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

        returns = pd.to_numeric(
            df[perf_col],
            errors="coerce"
        ).dropna()

        ytd = pd.to_numeric(
            df[ytd_col],
            errors="coerce"
        ).dropna()

        if len(returns) == 0:
            continue

        # conversion éventuelle %
        if abs(returns.mean()) > 0.20:
            returns = returns / 100

        if len(ytd) > 0 and abs(ytd.iloc[-1]) > 20:
            perf_ytd = ytd.iloc[-1] / 100
        else:
            perf_ytd = ytd.iloc[-1]

        volatility = (
            returns.std()
            * np.sqrt(52)
        )

        sharpe = 0

        if volatility > 0:

            sharpe = (
                returns.mean() * 52
            ) / volatility

        perf_annualisee = (
            (1 + perf_ytd)
            ** (52 / len(returns))
            - 1
        )

        result.append({

            "Fonds": fonds,

            "Perf Hebdo":
            returns.iloc[-1],

            "Perf YTD":
            perf_ytd,

            "Perf Annualisée":
            perf_annualisee,

            "Volatilité":
            volatility,

            "Sharpe":
            sharpe

        })

    return pd.DataFrame(result)
