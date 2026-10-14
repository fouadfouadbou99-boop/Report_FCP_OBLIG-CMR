import numpy as np


def compute_committee_kpis(nav, benchmark, sensitivity):

    returns = nav.pct_change().dropna()

    bench_returns = benchmark.pct_change().dropna()

    active_returns = returns - bench_returns

    tracking_error = active_returns.std() * np.sqrt(52)

    information_ratio = 0

    if tracking_error != 0:

        information_ratio = (
            active_returns.mean() * 52
        ) / tracking_error

    vol = returns.std() * np.sqrt(52)

    sharpe = 0

    if vol != 0:

        sharpe = (
            returns.mean() * 52
        ) / vol

    var95 = np.percentile(
        returns,
        5
    )

    cvar95 = returns[
        returns <= var95
    ].mean()

    drawdown = (
        nav / nav.cummax() - 1
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
