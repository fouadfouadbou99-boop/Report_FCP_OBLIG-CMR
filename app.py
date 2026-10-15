import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard FCP Obligataires",
    layout="wide"
)

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
    return r.mean() * 52


def annual_vol(r):
    return r.std() * np.sqrt(52)


def sharpe_ratio(r, rf=0):
    vol = annual_vol(r)

    if vol == 0 or np.isnan(vol):
        return np.nan

    return (annual_return(r) - rf) / vol


def sortino_ratio(r, rf=0):

    downside = r[r < 0]

    if len(downside) == 0:
        return np.nan

    downside_vol = downside.std() * np.sqrt(52)

    if downside_vol == 0:
        return np.nan

    return (annual_return(r) - rf) / downside_vol


def historical_var(r):
    return np.percentile(r.dropna(), 5)


def cvar(r):

    var = historical_var(r)

    losses = r[r <= var]

    if len(losses) == 0:
        return np.nan

    return losses.mean()


def max_drawdown(r):

    wealth = (1 + r.fillna(0)).cumprod()

    running_max = wealth.cummax()

    drawdown = (wealth - running_max) / running_max

    return drawdown.min()


def tracking_error(portfolio, benchmark):

    active = portfolio - benchmark

    return active.std() * np.sqrt(52)


def information_ratio(portfolio, benchmark):

    active = portfolio - benchmark

    te = active.std() * np.sqrt(52)

    if te == 0 or np.isnan(te):
        return np.nan

    return (active.mean() * 52) / te


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
            "BONDS": "Perf Hebdo BONDS",
            "OBLIGATIONS": "Perf Hebdo Obligations"
        }

        benchmark_col = "Weekly Perf"

        resultats = []

        if benchmark_col in df_perf.columns:

            benchmark = pd.to_numeric(
                df_perf[benchmark_col],
                errors="coerce"
            )

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

                if len(r) < 2:
                    continue

                ytd = np.nan

                ytd_col = col.replace(
                    "Perf Hebdo",
                    "Perf YTD"
                )

                if ytd_col in df_perf.columns:

                    ytd_series = pd.to_numeric(
                        df_perf[ytd_col],
                        errors="coerce"
                    ).dropna()

                    if not ytd_series.empty:
                        ytd = ytd_series.iloc[-1]

                resultats.append({

                    "Fonds": fund,

                    "Perf YTD": ytd,

                    "Perf Annualisée":
                        annual_return(r),

                    "Volatilité":
                        annual_vol(r),

                    "Sharpe":
                        sharpe_ratio(r),

                    "Sortino":
                        sortino_ratio(r),

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

        kpi_df = pd.DataFrame(resultats)

        if not kpi_df.empty:

            st.subheader("Matrice KPI")

            st.dataframe(
                kpi_df.style.format({
                    "Perf YTD": "{:.2%}",
                    "Perf Annualisée": "{:.2%}",
                    "Volatilité": "{:.2%}",
                    "Sharpe": "{:.2f}",
                    "Sortino": "{:.2f}",
                    "VaR 95%": "{:.2%}",
                    "CVaR": "{:.2%}",
                    "Max Drawdown": "{:.2%}",
                    "Tracking Error": "{:.2%}",
                    "Information Ratio": "{:.2f}"
                }),
                use_container_width=True
            )

            classement = kpi_df.sort_values(
                by="Sharpe",
                ascending=False
            )

            st.subheader("Classement")

            st.dataframe(
                classement,
                use_container_width=True
            )

            fig1 = px.bar(
                kpi_df,
                x="Fonds",
                y="Perf YTD",
                color="Fonds",
                title="Performance YTD"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            base100 = pd.DataFrame()

            cols_perf = {
                "SANADATE": "Perf Hebdo Sanadate",
                "BONDS": "Perf Hebdo BONDS",
                "OBLIGATIONS": "Perf Hebdo Obligations",
                "MBI MT": "Weekly Perf"
            }

            for nom, col in cols_perf.items():

                if col in df_perf.columns:

                    serie = pd.to_numeric(
                        df_perf[col],
                        errors="coerce"
                    ).fillna(0)

                    base100[nom] = (
                        100 * (1 + serie).cumprod()
                    )

            if not base100.empty:

                fig2 = px.line(
                    base100,
                    title="Evolution Base 100"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            if df_sensi is not None:

                st.subheader("Sensibilités")

                sensi_data = []

                for col in df_sensi.columns[1:]:

                    val = pd.to_numeric(
                        df_sensi[col],
                        errors="coerce"
                    ).mean()

                    sensi_data.append({
                        "Fonds": col,
                        "Sensibilité": val
                    })

                sensi_df = pd.DataFrame(sensi_data)

                st.dataframe(
                    sensi_df,
                    use_container_width=True
                )

            st.subheader("Commentaire Comité")

            meilleur = classement.iloc[0]

            commentaire = f"""
Le fonds le mieux classé selon le ratio de Sharpe est
{meilleur['Fonds']}.

La performance annualisée ressort à
{meilleur['Perf Annualisée']:.2%}.

La volatilité observée atteint
{meilleur['Volatilité']:.2%}.

Le ratio de Sharpe s'établit à
{meilleur['Sharpe']:.2f},
ce qui traduit la meilleure efficacité
risque/rendement de l'échantillon.
"""

            st.info(commentaire)

        else:

            st.warning(
                "Aucune donnée exploitable trouvée."
            )

    except Exception as e:

        st.error(
            f"Erreur de traitement : {e}"
        )
