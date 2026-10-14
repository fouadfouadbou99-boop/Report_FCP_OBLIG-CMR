import numpy as np
import pandas as pd

def calculate_performance(returns):

    cumulative = (1 + returns).cumprod() - 1

    annualized_return = (
        (1 + cumulative.iloc[-1]) **
        (52 / len(returns))
    ) - 1

    volatility = returns.std() * np.sqrt(52)

    sharpe = np.nan

    if volatility != 0:
        sharpe = annualized_return / volatility

    return {
        "Performance Cumulée": cumulative.iloc[-1],
        "Performance Annualisée": annualized_return,
        "Volatilité": volatility,
        "Sharpe": sharpe
    }
