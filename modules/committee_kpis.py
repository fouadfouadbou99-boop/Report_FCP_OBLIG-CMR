import numpy as np


def compute_committee_kpis(
    nav,
    benchmark,
    sensitivity
):

    nav = nav.dropna()

    benchmark = benchmark.dropna()

    r = nav.pct_change().dropna()

    rb = benchmark.pct_change().dropna()

    n = min(len(r), len(rb))

    r = r.tail(n)

    rb = rb.tail(n)

    active = r - rb

    tracking_error = (
        active.std()
        * np.sqrt(52)
    )

    information_ratio = 0

    if tracking_error > 0:

        information_ratio = (
            active.mean() * 52
        ) / tracking_error

    volatility = (
        r.std()
        * np.sqrt(52)
    )

    sharpe = 0

    if volatility > 0:

        sharpe = (
            r.mean() * 52
        ) / volatility

    var95 = np.percentile(
        r,
        5
    )

    cvar95 = r[r <= var95].mean()

    drawdown = (
        nav /
        nav.cummax()
        - 1
    )

    max_drawdown = drawdown.min()

    dv01 = sensitivity * 0.0001

    convexity = (
        sensitivity ** 2
    ) / 100

    return {

        "tracking_error": tracking_error,

        "information_ratio": information_ratio,

        "sharpe": sharpe,

        "var95": var95,

        "cvar95": cvar95,

        "max_drawdown": max_drawdown,

        "dv01": dv01,

        "convexity": convexity

    }
