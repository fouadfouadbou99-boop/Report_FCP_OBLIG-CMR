import numpy as np


def compute_committee_kpis(
        fund_returns,
        benchmark_returns,
        sensitivity):

    fund_returns = fund_returns.dropna()
    benchmark_returns = benchmark_returns.dropna()

    if abs(fund_returns.mean()) > 1:
        fund_returns = fund_returns / 100

    if abs(benchmark_returns.mean()) > 1:
        benchmark_returns = benchmark_returns / 100

    n = min(
        len(fund_returns),
        len(benchmark_returns)
    )

    fund_returns = fund_returns.tail(n)
    benchmark_returns = benchmark_returns.tail(n)

    active = (
        fund_returns
        - benchmark_returns
    )

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
        fund_returns.std()
        * np.sqrt(52)
    )

    sharpe = 0

    if volatility > 0:

        sharpe = (
            fund_returns.mean()
            * 52
        ) / volatility

    var95 = np.percentile(
        fund_returns,
        5
    )

    cvar95 = fund_returns[
        fund_returns <= var95
    ].mean()

    dv01 = (
        float(sensitivity)
        * 0.0001
    )

    convexity = (
        float(sensitivity) ** 2
    ) / 100

    return {

        "tracking_error": tracking_error,

        "information_ratio": information_ratio,

        "sharpe": sharpe,

        "var95": var95,

        "cvar95": cvar95,

        "max_drawdown": 0,

        "dv01": dv01,

        "convexity": convexity

    }
