import pandas as pd
import nump***s np

def max_drawdown(nav):

  ***d = nav/nav.cummax()-1

    retu***dd.min()

def compute_risk_metri***
        perf_df,
        sensi_***):

    result = []

    mapping***{

        "SANADATE":"SAN***TE_VL",
***     "BONDS":"BONDS_VL",
***     "***IGATIONS":"OBLIG_VL"

    }

   ***r nom,col in mapping.items():

 ***    nav = perf_df[col].dropna()
***      r = nav.pct_change().dropn***

        var95 = np.percentile(***)

        var99 = np.percentile***1)

        cvar95 = (
         ***r[r<=var95].mean()
        )

  ***   cvar99 = (
            r[r<=v***9].mean()
        )

        vol***n = (
            r.std***            * np.sqrt(52)
      ***

        mdd***max_drawdown(nav)

        resul***ppend({

            "Fonds":nom***            "Volatilité":vol_ann***            "VaR95":var95,

    ***     "VaR99":var99,

           *****R95":cvar95,

            "CVaR9***cvar99,

            "Max Drawdo***:mdd,

            "***st Week":r.min(),

            "***t Week":r.max(),

            "S***ness":r.skew(),

            "***tosis":r.kurt()

        })

   ***turn pd.DataFrame(result)
