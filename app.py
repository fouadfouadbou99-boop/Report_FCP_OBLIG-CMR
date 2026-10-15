import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard FCP Obligataires",
    layout="wide"
)

RISK_FREE_RATE = 0.025


# =====================================================
# CHARGEMENT
# =====================================================

@st.cache_data
def load_excel(file):

    xls = pd.ExcelFile(file)

    sheets = xls.sheet_names

    df_perf = pd.read_excel(
        file,
        sheet_name=sheets[0]
    )

    df_sensi = None

    if len(sheets) > 1:

        df_sensi = pd.read_excel(
            file,
            sheet_name=sheets[1]
        )

    return df_perf, df_sensi


# =====================================================
# KPI
# =====================================================

def annual_return(r):

    r = r.dropna()

    if len(r) == 0:
        return np.nan

    return (1 + r).prod() ** (52 / len(r)) - 1


def annual_vol(r):

    r = r.dropna()

    if len(r) < 2:
        return np.nan

    return r.std() * np.sqrt(52)


def sharpe_ratio(r):

    ret = annual_return(r)
    vol = annual_vol(r)

    if pd.isna(vol) or vol == 0:
        return np.nan

    return (ret - RISK_FREE_RATE) / vol


def sortino_ratio(r):

    downside = r[r < 0]

    if len(downside) < 2:
        return np.nan

    downside_vol = downside.std() * np.sqrt(52)

    if downside_vol == 0:
        return np.nan

    return (annual_return(r) - RISK_FREE_RATE) / downside_vol


def historical_var(r):

    r = r.dropna()

    if len(r) == 0:
        return np.nan

    return np.percentile(r, 5)


def var99(r):

    r = r.dropna()

    if len(r) == 0:
        return np.nan

    return np.percentile(r, 1)


def cvar(r):

    var = historical_var(r)

    losses = r[r <= var]

    if len(losses) == 0:
        return np.nan

    return losses.mean()


def max_drawdown(r):

    wealth = (1 + r.fillna(0)).cumprod()

    peak = wealth.cummax()

    drawdown = (wealth - peak) / peak

    return drawdown.min()


def calmar_ratio(r):

    dd = abs(max_drawdown(r))

    if dd == 0:
        return np.nan

    return annual_return(r) / dd


def tracking_error(portfolio, benchmark):

    active = portfolio - benchmark

    return active.std() * np.sqrt(52)


def information_ratio(portfolio, benchmark):

    active = portfolio - benchmark

    te = active.std() * np.sqrt(52)

    if te == 0:
        return np.nan

    return (active.mean() * 52) / te


def beta(portfolio, benchmark):

    cov = np.cov(portfolio, benchmark)[0, 1]

    var_bench = np.var(benchmark)

    if var_bench == 0:
        return np.nan

    return cov / var_bench


def alpha(portfolio, benchmark):

    return annual_return(portfolio) - annual_return(benchmark)


# =====================================================
# INTERFACE
# =====================================================

st.title("📊 Dashboard FCP Obligataires")

uploaded_file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        df_perf, df_sensi = load_excel(uploaded_file)

        st.success("Fichier chargé avec succès")

        st.subheader("Aperçu des données")
        st.dataframe(df_perf.head())

        fonds = {
            "SANADATE": "Perf Hebdo Sanadate",
            
