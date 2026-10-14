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
    plot_risk_return
)

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

from modules.committee_kpis import (
    compute_committee_kpis
)

committee = compute_committee_kpis(

    perf_df["SANADATE_VL"],

    perf_df["BONDS_VL"],

    sensi_df["SANADATE"].iloc[-1]

)

te = committee["tracking_error"]

ir = committee["information_ratio"]

sharpe = committee["sharpe"]

var95 = committee["var95"]

cvar95 = committee["cvar95"]

mdd = committee["max_drawdown"]

dv01 = committee["dv01"]

convexity = committee["convexity"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Dashboard",
            "Performances",
            "Risques",
            "Sensibilité",
            "Comité"
        ]
    )

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    with tab1:

        st.subheader("KPIs Exécutifs")

        st.dataframe(
            perf_metrics,
            width="stretch"
        )

        st.subheader(
            "KPIs Comité d'Investissement"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Tracking Error",
                f"{te:.2%}"
            )

        with col2:
            st.metric(
                "Information Ratio",
                f"{ir:.2f}"
            )

        with col3:
            st.metric(
                "DV01",
                f"{dv01:.4f}"
            )

        with col4:
            st.metric(
                "Convexité",
                f"{convexity:.2f}"
            )

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric(
                "VaR 95 %",
                f"{var95:.2%}"
            )

        with col6:
            st.metric(
                "CVaR 95 %",
                f"{cvar95:.2%}"
            )

        with col7:
            st.metric(
                "Max Drawdown",
                f"{mdd:.2%}"
            )

        with col8:
            st.metric(
                "Sharpe",
                f"{sharpe:.2f}"
            )

        st.plotly_chart(
            plot_risk_return(
                perf_metrics
            ),
            width="stretch"
        )
from modules.exports_excel import (
    export_excel
)

excel_file = export_excel(
    perf_metrics,
    risk_metrics
)

st.download_button(

    "📥 Export Excel",

    data=excel_file,

    file_name="Rapport_FCP.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
    # --------------------------------------------------
    # PERFORMANCES
    # --------------------------------------------------

    with tab2:

        st.plotly_chart(
            plot_nav(perf_df),
            width="stretch"
        )

        st.plotly_chart(
            plot_performance(perf_df),
            width="stretch"
        )

    # --------------------------------------------------
    # RISQUES
    # --------------------------------------------------

    with tab3:

        st.dataframe(
            risk_metrics,
            width="stretch"
        )

        st.plotly_chart(
            plot_drawdown(
                perf_df
            ),
            width="stretch"
        )

    # --------------------------------------------------
    # SENSIBILITES
    # --------------------------------------------------

    with tab4:

        st.plotly_chart(
            plot_sensitivity(
                sensi_df
            ),
            width="stretch"
        )

    # --------------------------------------------------
    # COMITE
    # --------------------------------------------------

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
