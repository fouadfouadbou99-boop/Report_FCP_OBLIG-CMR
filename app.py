import streamlit as st
from modules.data_loader import load_data
from modules.performance import compute_performance
from modules.risk import compute_risk_metrics
from modules.committee_comments import generate_comment
from modules.charts import (
    plot_nav,
    plot_performance,
    plot_drawdown,
    plot_sensitivity,
    plot_risk_return,
)

st.set_page_config(
    page_title="FCP Obligataire Dashboard",
    layout="wide"
)

st.title("FCP Obligataire - Tableau de Bord")

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    perf_df, sensi_df = load_data(uploaded_file)

    perf_metrics = compute_performance(perf_df)

    risk_metrics = compute_risk_metrics(perf_df, sensi_df)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard",
        "Performances",
        "Risques",
        "Sensibilités",
        "Comité"
    ])

    with tab1:

        st.subheader("KPIs Exécutifs")
        st.dataframe(perf_metrics)

        st.plotly_chart(
            plot_risk_return(perf_metrics),
            use_container_width=True
        )

    with tab2:

        st.plotly_chart(
            plot_nav(perf_df),
            use_container_width=True
        )

        st.plotly_chart(
            plot_performance(perf_df),
            use_container_width=True
        )

    with tab3:

        st.dataframe(risk_metrics)

        st.plotly_chart(
            plot_drawdown(perf_df),
            use_container_width=True
        )

    with tab4:

        st.plotly_chart(
            plot_sensitivity(sensi_df),
            use_container_width=True
        )

    with tab5:

        commentaire = generate_comment(
            perf_metrics,
            risk_metrics
        )

        st.markdown(commentaire)
