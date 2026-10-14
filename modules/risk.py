import numpy as np

def var_historique(series, confidence=0.95):

    return np.percentile(
        series.dropna(),
        (1-confidence)*100
    )

def c*ar*series, confidence=0.95):

    var*= var_historique(
        series,
*       confidence
    )

    retur* series[
        series <= var
    ].mean()

def max_drawdown(series)*

    cumulative = (1 + series).cu*prod()

    running_max = cumulati*e.cummax()

    drawdown = (
     *  cumulative-running_max
    ) / r*nning_max

    return drawdown.min*)

def tracking_error(fund, benchmark):

    diff = fund - benchmark

    return diff.std()*np.sqrt(52)

def information_ratio(fund, benchmark):

    alpha = (
        fund.mean()
        - benchmark.mean()
    ) * 52

    te = tracking_error(
        fund,
        benchmark
    )

    return alpha/te if te else 0
