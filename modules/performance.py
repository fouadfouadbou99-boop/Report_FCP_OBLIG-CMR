import pandas as pd
import numpy as np
from scipy.stats import linregress

def sharpe_ratio(r):

    vol = r.std()

    if vol == 0:
        return 0

    return r.mean()/vol

def sortino_ratio(r):

    downside = r[r < 0]

    if len(downside) == 0:
        return 0

    downside_std = downside.std()

    if downside_std == 0:
        return 0

    return r.mean()/downside_std

def annualized_return(r):

    return ((1+r).prod())**(52/len(r))-1

def compute_perfor**nce(df):

    fonds = {
        "**NADATE":"SANADATE_VL",
        "B**DS":"BONDS_VL",
        "OBLIGATI**S":"OBLIG_VL"
    }

    result =**]

    for nom,col in fonds.items**:

        nav = df[col].dropna()**        r = nav.pct_change().drop**()

        perf_ann = annualized**eturn(r)

        vol = r.std()*n***qrt(52)

        sharpe = sharpe***tio(r)

        sortino = sortin***atio(r)

        perf_total = (
***         nav.iloc[-1]/nav.iloc[0]-1
        )

        mdd = (
    ***     nav/nav.cummax()-1
        ***in()

        calmar = 0

      ***f abs(mdd) > 0:
            calm***= perf_ann/abs(mdd)

        res***.append({

            "Fonds":n***

            "Perf Cumulée":per***otal,

            "Perf Annuali***":perf_ann,

            "Volati***é":vol,

            "Sharpe":sh***e,

            "Sortino":sortin***
            "Max Drawdown":mdd,***           "Calmar":calmar

    *** })

    return pd.DataFrame(res***)
