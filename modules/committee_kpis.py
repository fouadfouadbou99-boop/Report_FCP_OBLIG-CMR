import numpy as np


def compute_committee_kpis(
        nav,
        benchmark,
        sensitivity):

    returns = nav.pct_change().dropna()

    bench = benchmark.pct_change().dropna()

    n = min(len(returns), len(bench))

    returns = returns[-n:]
    bench = bench[-n:]

    active = returns - bench

    tracking_error = (
        active.std()
        * np.sqrt(52)
    )

    information_ratio = 0

    if tracking_error > 0:

        information_ratio = (
            active.mean()
            * 52
        ) / tracking_error

    volatility = (
        returns.std()
        * np.sqrt(52)
    )

    sharpe = 0

    if volatility > 0:

        sharpe = (
            returns.mean()
            * 52
        ) / volatility

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

    return {

        "tracking_error": tracking_error,

        "information_ratio": information_ratio,

        "sharpe": sharpe,

        "var95": var95,

        "cvar95": cvar95,

        "max_drawdown": max_drawdown,

        "sensitivity": sensitivity

    }
