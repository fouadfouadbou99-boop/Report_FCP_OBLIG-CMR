import pandas as pd
import numpy as np

def compute_performance(df):

    fonds = {
        "SANADATE":"SANADATE_PERF_W",
        "BONDS":"BONDS_PERF_W",
        "OBLIGATIONS":"OBLIG_PERF_W"
    }

    result = []

    for nom,col in fonds.items():

        r = df[col].dropna()

        vol = r.std()*np.sqrt(52)

        annual_return*= (
            (1+r.mean())**52
 ***    )-1

        sharpe = 0

   ***  if vol != 0:
            sharp*** annual_return/vol

        resu***append({
            "Fonds":nom***           "Perf anualisée":annu***return,
            "Volatilité"***l,
            "Sharpe":sharpe
 ***    })

    return pd.DataFrame(***ult)
