import streamlit as st

from modules.data_loader import load_data
from modules.performance import compute_performance
from modules.risk import compute_risk_metrics

from modules.charts import (
    plot_nav,
    plot_performance,
    plot_drawdown,
    plot_sensitivity,
    plot_risk_return
)

from modules.committee_comments import generate_comment

st.set_page_config(
    page_title="FCP Obligataire",
    layout="wide"
)

st.title("📊 Dashboard FCP Obligataire")

fichier = st.file_uploader(
    "Importer le fichier KPI",
    type=["xlsx"]
)

if fichier:

    perf_df, sensi_df = load_data(fichier)

    perf_metrics = compute_performance(perf_df)

    risk_metrics = compute_risk_metrics(
        perf_df,
        sensi_df
    )

    commentaire = generate_comment(
        perf_metrics,
        risk_metrics
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Dashboard",
            "Performances",
            "Risques",
            "Sensibilité",
            "Comité"
        ]
    )

    with tab1:

        st.subheader("KPIs Exécutifs")

        st.dataframe(
            perf_metrics,
            width="stretch"
        )

        st.plotly_chart(
            plot_risk_return(
                perf_metrics
            ),
            width="stretch"
        )

    with tab2:

        st.plotly_chart(
            plot_nav(perf_df),
            width="stretch"
        )

        st.plotly_chart(
            plot_performance(perf_df),
            width="stretch"
        )

    with tab3:

        st.dataframe(
            risk_metrics,
            width="stretch"
        )

        st.plotly_chart(
            plot_drawdown(perf_df),
            width="stretch"
        )

    with tab4:

        st.plotly_chart(
            plot_sensitivity(
                sensi_df
            ),
            width="stretch"
        )

    with tab5:

        st.markdown(commentaire)

        st.dataframe(
            perf_metrics,
            width="stretch"
        )

        st.dataframe(
            risk_metrics,
            width="stretch"
        )

else:

    st.info(
        "Importer FCP_Obligataire_KPIs_Report.xlsx"
    )
