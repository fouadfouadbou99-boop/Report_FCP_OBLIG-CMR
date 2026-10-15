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

                mask = r.notna() & benchmark.notna()

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

                    ytd_values = pd.to_numeric(
                        df_perf[ytd_col],
                        errors="coerce"
                    ).dropna()

                    if not ytd_values.empty:
                        ytd = ytd_values.iloc[-1]

                resultats.append({

                    "Fonds": fund,
                    "Perf YTD": ytd,
                    "Perf Annualisée": annual_return(r),
                    "Volatilité": annual_vol(r),
                    "Sharpe": sharpe_ratio(r),
                    "Sortino": sortino_ratio(r),
                    "Alpha": alpha(r, b),
                    "Beta": beta(r, b),
                    "VaR95": historical_var(r),
                    "VaR99": var99(r),
                    "CVaR": cvar(r),
                    "Max Drawdown": max_drawdown(r),
                    "Calmar": calmar_ratio(r),
                    "Tracking Error": tracking_error(r, b),
                    "Information Ratio": information_ratio(r, b)

                })

        kpi_df = pd.DataFrame(resultats)

        if not kpi_df.empty:

            st.subheader("Matrice KPI")

            st.dataframe(
                kpi_df.style.format({
                    "Perf YTD": "{:.2%}",
                    "Perf Annualisée": "{:.2%}",
                    "Volatilité": "{:.2%}",
                    "Alpha": "{:.2%}",
                    "Sharpe": "{:.2f}",
                    "Sortino": "{:.2f}",
                    "Calmar": "{:.2f}",
                    "VaR95": "{:.2%}",
                    "VaR99": "{:.2%}",
                    "CVaR": "{:.2%}",
                    "Max Drawdown": "{:.2%}",
                    "Tracking Error": "{:.2%}",
                    "Information Ratio": "{:.2f}"
                }),
                use_container_width=True
            )

            classement = kpi_df.copy()

            classement["Score"] = (
                0.30 * classement["Perf YTD"].rank(pct=True)
                + 0.25 * classement["Sharpe"].rank(pct=True)
                + 0.15 * classement["Sortino"].rank(pct=True)
                + 0.10 * classement["Calmar"].rank(pct=True)
                + 0.10 * (-classement["Tracking Error"]).rank(pct=True)
                + 0.10 * (-classement["Max Drawdown"]).rank(pct=True)
            )

            classement = classement.sort_values(
                "Score",
                ascending=False
            )

            classement.insert(
                0,
                "Rang",
                range(1, len(classement) + 1)
            )

            st.subheader("Classement Global")

            st.dataframe(
                classement[
                    [
                        "Rang",
                        "Fonds",
                        "Perf YTD",
                        "Sharpe",
                        "Sortino",
                        "Calmar",
                        "Score"
                    ]
                ].style.format({
                    "Perf YTD": "{:.2%}",
                    "Sharpe": "{:.2f}",
                    "Sortino": "{:.2f}",
                    "Calmar": "{:.2f}",
                    "Score": "{:.2f}"
                }),
                use_container_width=True
            )

            fig1 = px.bar(
                kpi_df,
                x="Fonds",
                y="Perf YTD",
                color="Fonds",
                title="Performance YTD"
            )

            st.plotly_chart(fig1, use_container_width=True)

            base100 = pd.DataFrame()

            if "Date" in df_perf.columns:
                base100["Date"] = pd.to_datetime(df_perf["Date"])

            perf_cols = {
                "SANADATE": "Perf Hebdo Sanadate",
                "BONDS": "Perf Hebdo BONDS",
                "OBLIGATIONS": "Perf Hebdo Obligations",
                "MBI MT": "Weekly Perf"
            }

            for nom, col in perf_cols.items():

                if col in df_perf.columns:

                    serie = pd.to_numeric(
                        df_perf[col],
                        errors="coerce"
                    ).fillna(0)

                    base100[nom] = (
                        100 * (1 + serie).cumprod()
                    )

            if not base100.empty and "Date" in base100.columns:

                fig2 = px.line(
                    base100,
                    x="Date",
                    y=[
                        c for c in base100.columns
                        if c != "Date"
                    ],
                    title="Evolution Base 100"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            if df_sensi is not None:

                st.subheader("Sensibilités Moyennes")

                valid_cols = [
                    "SANADATE",
                    "BONDS",
                    "OBLIGATIONS",
                    "MBI MT"
                ]

                sensi_data = []

                for col in valid_cols:

                    if col in df_sensi.columns:

                        sensi_data.append({

                            "Fonds": col,

                            "Sensibilité":
                            pd.to_numeric(
                                df_sensi[col],
                                errors="coerce"
                            ).mean()

                        })

                sensi_df = pd.DataFrame(sensi_data)

                st.dataframe(
                    sensi_df.style.format({
                        "Sensibilité": "{:.2f}"
                    }),
                    use_container_width=True
                )

            st.subheader("Commentaire Comité")

            meilleur = classement.iloc[0]

            commentaire = f"""
Le fonds actuellement le mieux classé est {meilleur['Fonds']}.

Sa performance YTD ressort à {meilleur['Perf YTD']:.2%}
pour une performance annualisée de
{meilleur['Perf Annualisée']:.2%}.

Le ratio de Sharpe atteint
{meilleur['Sharpe']:.2f}
et le ratio de Sortino
{meilleur['Sortino']:.2f}.

Le classement tient compte simultanément
du rendement, du Sharpe, du Sortino,
du Calmar, du Tracking Error
et du Drawdown.
"""

            st.info(commentaire)

    except Exception as e:

        st.error(f"Erreur de traitement : {e}")
