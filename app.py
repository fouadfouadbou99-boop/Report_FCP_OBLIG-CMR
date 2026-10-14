import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.performance import calculate_performance
from modules.risk import (
    var_historique,
    cvar,
    max_drawdown
)
from modules.commentary import (
    generate_commentary
)
from modules.stress_test import (
    stress_duration
)

st.set_page_config(
    page_title="Dashboard FCP Obligataire",
    layout="wide"
)

st.title(
    "Tableau de Bord Fonds Obligataire"
)

file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if file:

    sheets = load_data(file)

    st.success(
        "Fichier chargé avec succès"
    )

    sheet_name = st.selectbox(
        "Choisir un onglet",
        list(sheets.keys())
    )

    df = sheets[sheet_name]

    st.dataframe(df)

    cols = df.columns.tolist()

    rendement = st.selectbox(
        "Colonne Rendement",
        cols
    )

    serie = pd.to_numeric(
        df[rendement],
        errors="coerce"
    ).dropna()

    perf = calculate_performance(
        serie
    )

    st.subheader(
        "KPIs de Performance"
    )

    st.metric(
        "Perf annualisée",
        f"{perf['Performance Annualisée']:.2%}"
    )

    st.metric(
        "Volatilité",
        f"{perf['Volatilité']:.2%}"
    )

    st.metric(
        "Sharpe",
        f"{perf['Sharpe']:.2f}"
    )

    st.subheader(
        "KPIs de Risque"
    )

    st.metric(
        "VaR 95 %",
        f"{var_historique(serie):.2%}"
    )

    st.metric(
        "CVaR",
        f"{cvar(serie):.2%}"
    )

    st.metric(
        "Maximum Drawdown",
        f"{max_drawdown(serie):.2%}"
    )

    commentaire = generate_commentary(
        perf
    )

    st.subheader(
        "Commentaire Comité"
    )

    st.write(commentaire)
