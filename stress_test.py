import pandas as pd

def stress_duration(nav, duration):

    scenarios = [
        0.25,
        0.50,
        1.00,
        1.50,
        2.00
    ]

    rows = []

    for s in scenarios:

        impact_pct = -duration*s

        impact_value = nav*impact_pct/100

        rows.append({
            "Choc Taux (%)": s,
            "Impact %": impact_pct,
            "Impact VL": impact_value
        })

    return pd.DataFrame(rows)
``
