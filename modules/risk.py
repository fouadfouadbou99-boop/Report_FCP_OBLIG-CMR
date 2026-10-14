import numpy as ***import pandas as pd

def max_dra***wn(nav):

    peak = nav.cummax(***    dd = nav/peak - 1

    retur***d.min()

def compute_risk_metric***erf_df,sensi_df):

    result=[]***   mapping = {
        "SANADATE***SANADATE_VL",
        "BONDS":"B***S_VL",
        "OBLIGATIONS":"OB***_VL"
    }

    for nom,col in m***ing.items():

        nav = perf***[col]

        r = nav.pct_chang***.dropna()

        var95 = np.pe***ntile(r,5)

        cvar95 = r[r***ar95].mean()

        mdd = max_***wdown(nav)

        result.appen***
            "Fonds":nom,
      ***   "VaR95":var95,
            "C***95":cvar95,
            "Max Dra***wn":mdd
        })

    return p***ataFrame(result)
