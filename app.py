import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard FCP Obligataires",
    layout="wide"
)

# =====================================================
# CHARGEMENT DATA
# =====================================================

@st.cache_data
def load_data(file):

    xls = pd.ExcelFile(file)

    perf_sheet = xls.sheet_names[0]
    sensi_sheet = xls.sheet_names[1]

    df_perf = pd.read_excel(
        file,
        sheet_name=perf_sheet
    )

    df_sensi = pd.read_excel(
        file,
        sheet_name=sensi_sheet
    )

    return df_perf, df_sensi


# =====================================================
# FONCTIONS RISQUE / RENDEMENT
# =====================================================

def annual_return(r):

    return r.mean() * 52


def annual_vol(r):

    return r.std() * np.sqrt(52)


def sharpe(r, rf=0):

    vol = annual_vol(r)

    if vol == 0:
        return np.nan

    return (annual_return(r) - rf) / vol


def sortino(r, rf=0):

    downside = r[r < 0]

    if len(downside) == 0:
        return np.nan

    dvol = downside.std() * np.sqrt(52)

    return (annual_return(r) - rf) / dvol


def historical_var(r):

    return np.percentile(r, 5)


def cvar(r):

    var = historical_var(r)

    return r[r <= var].mean()


def max_drawdown(r):

    wealth = (1 + r).cumprod()

    peak = wealth.cummax()

    dd = (wealth - peak) / peak

    return dd.min()


def tracking_error(portfolio, benchmark):

    excess = portfolio - benchmark

    return excess.std() * np.sqrt(52)


def information_ratio(portfolio, benchmark):

    active = portfolio - benchmark

    te = active.std() * np.sqrt(52)

    if te == 0:
        return np.nan

    return (active.mean() * 52) / te


# =====================================================
# INTERFACE
# =====================================================

st.title("📊 Dashboard FCP Obligataires")

uploaded = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded:

    df_perf, df_sensi = load_data(uploaded)

    # =================================================
    # DETECTION AUTOMATIQUE
    # =================================================

    fonds = {
        "SANADATE": "Perf Hebdo Sanadate",
        "BONDS": "Perf Hebdo BONDS",
        "OBLIGATIONS": "Perf Hebdo Obligations"
    }

    benchmark_col = "Weekly Perf"

    benchmark = pd.to_numeric(
        df_perf[benchmark_col],
        errors="coerce"
    )

    # ===============================================
    # KPI
    # ===============================================

    kpis = []

    for fund, col in fonds.items():

        if col not in df_perf.columns:
            continue

        r = pd.to_numeric(
            df_perf[col],
            errors="coerce"
        )

        mask = (
            r.notna()
            &
            benchmark.notna()
        )

        r = r[mask]
        b = benchmark[mask]

        ytd_col = col.replace(
            "Perf Hebdo",
            "Perf YTD"
        )

        ytd = np.nan

        if ytd_col in df_perf.columns:

            ytd = pd.to_numeric(
                df_perf[ytd_col],
                errors="coerce"
            ).iloc[-1]

        kpis.append({

            "Fonds": fund,

            "Perf YTD":
                ytd,

            "Perf Annualisée":
                annual_return(r),

            "Volatilité":
                annual_vol(r),

            "Sharpe":
                sharpe(r),

            "Sortino":
                sortino(r),

            "VaR 95%":
                historical_var(r),

            "CVaR":
                cvar(r),

            "Max Drawdown":
                max_drawdown(r),

            "Tracking Error":
                tracking_error(r, b),

            "Information Ratio":
                information_ratio(r, b)

        })

    kpi_df = pd.DataFrame(kpis)

    # =================================================
    # DASHBOARD KPI
    # =================================================

    st.subheader("Classement des Fonds")

    classement = kpi_df.sort_values(
        "Sharpe",
        ascending=False
    )

    st.dataframe(
        classement.style.format({
            "Perf YTD":"{:.2%}",
            "Perf Annualisée":"{:.2%}",
            "Volatilité":"{:.2%}",
            "Sharpe":"{:.2f}",
            "Sortino":"{:.2f}",
            "VaR 95%":"{:.2%}",
            "CVaR":"{:.2%}",
            "Max Drawdown":"{:.2%}",
            "Tracking Error":"{:.2%}",
            "Information Ratio":"{:.2f}"
        }),
        use_container_width=True
    )

    # =================================================
    # GRAPHIQUE YTD
    # =================================================

    st.subheader("Performance YTD")

    fig = px.bar(
        kpi_df,
        x="Fonds",
        y="Perf YTD",
        color="Fonds",
        text_auto=".2%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =================================================
    # BASE 100
    # =================================================

    st.subheader("Evolution Base 100")

    perf_cols = {
        "SANADATE":"Perf Hebdo Sanadate",
        "BONDS":"Perf Hebdo BONDS",
        "OBLIGATIONS":"Perf Hebdo Obligations",
        "MBI MT":"Weekly Perf"
    }

    base100 = pd.DataFrame()

    for nom, col in perf_cols.items():

        if col in df_perf.columns:

            serie = pd.to_numeric(
                df_perf[col],
                errors="coerce"
            ).fillna(0)

            base100[nom] = (
                100 * (1 + serie).cumprod()
            )

    fig2 = px.line(
        base100,
        title="Comparaison Base 100"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =================================================
    # SENSIBILITE
    # =================================================

    st.subheader("Sensibilité Moyenne")

    sensi = []

    for col in df_sensi.columns:

        if col == df_sensi.columns[0\]:
            continue

        sensi.append({
            "Fonds": col,
            "Sensibilité":
            pd.to_numeric(
                df_sensi[col],
                errors="coerce"
            ).mean()
        })

    sensi_df = pd.DataFrame(sensi)

    st.dataframe(
        sensi_df.style.format({
            "Sensibilité":"{:.2f}"
        }),
        use_container_width=True
    )

    fig3 = px.bar(
        sensi_df,
        x="Fonds",
        y="Sensibilité",
        color="Fonds"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =================================================
    # COMMENTAIRES AUTOMATIQUES
    # =================================================

    st.subheader("Commentaire Comité de Gestion")

    meilleur = classement.iloc[0]

    commentaire = f"""
Le fonds le mieux classé selon le ratio de Sharpe est
{meilleur['Fonds']}.

Sa performance annualisée ressort à
{meilleur['Perf Annualisée']:.2%%}
pour une volatilité de
{meilleur['Volatilité'\]:.2%}.

Le ratio de Sharpe atteint
{meilleur['Sharpe'\]:.2f},
témoignant d'une meilleure efficacité
risque/rendement relativement aux autres
fonds étudiés.

L'analyse des sensibilités devra être
surveillée afin d'évaluer l'impact
d'un éventuel déplacement de la courbe
des taux sur les performances futures.
"""

    st.info(commentaire)
