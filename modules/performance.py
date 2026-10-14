import numpy as np
import pandas as pd

def annualized_return(r):

    return (1+r.mean())**52 - 1

def sharpe_ratio(r):

    vol = r.std()

    if vol == 0:
        return 0

    return r.mean() / vol

def compute_performance(df):

    result = pd.DataFrame()

    return result
