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

try:
    from modules.committee_kpis import compute_committee_kpis
except:
    compute_committee_kpis = None

try:
    from modules.exports_excel import export_excel
except:
    export_excel = None

try:
    from modules.exports_pdf import export_pdf
except:
    export_pdf = None


st.set_page_config(
    page_title="FCP Obligataire",
    layout="wide"
)

st.title("📊 Dashboard FCP Obligataire")

fichier = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if fichier is not None:

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

    # Valeurs par défaut
    te = 0
    ir = 0
    sharpe = 0
    var95 = 0
    cvar95 = 0
    mdd = 0
    dv01 = 0
    convexity = 0

    # KPI Comité
    if compute_committee_kpis is not None:

        try:

            committee = compute_committee_kpis(
                perf_df["SANADATE_VL"],
                perf_df["MBI_MT"],
                float(
                    sensi_df["SANADATE"]
                    .dropna()
                    .iloc[-1]
                )
            )

            te = committee["tracking_error"]
            ir = committee["information_ratio"]
            sharpe = committee["sharpe"]
            var95 = committee["var95"]
            cvar95 = committee["cvar95"]
            mdd = committee["max_drawdown"]
            dv01 = committee["dv01"]
            convexity = committee["convexity"]

        except Exception as e:

            st.warning(
                f"KPI Comité non disponibles : {e}"
            )

    # Exports
    excel_file = None
    pdf_file = None

    if export_excel is not None:

        try:

            excel_file = export_excel(
                perf_metrics,
                risk_metrics
            )

        except:
            pass

    if export_pdf is not None:

        try:

            pdf_file = export_pdf(
                commentaire
            )

        except:
            pass

    # Onglets
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Dashboard",
            "Performances",
            "Risques",
            "Sensibilité",
            "Comité"
        ]
    )

    # DASHBOARD

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

        col1.metric(
            "Tracking Error",
            f"{te:.2%}"
        )

        col2.metric(
            "Information Ratio",
            f"{ir:.2f}"
        )

        col3.metric(
            "DV01",
            f"{dv01:.4f}"
        )

        col4.metric(
            "Convexité",
            f"{convexity:.2f}"
        )

        col5, col6, col7, col8 = st.columns(4)

        col5.metric(
            "VaR 95%",
            f"{var95:.2%}"
        )

        col6.metric(
            "CVaR 95%",
            f"{cvar95:.2%}"
        )

        col7.metric(
            "Max Drawdown",
            f"{mdd:.2%}"
        )

        col8.metric(
            "Sharpe",
            f"{sharpe:.2f}"
        )

        st.plotly_chart(
            plot_risk_return(
                perf_metrics
            ),
            width="stretch"
        )

        st.subheader("Exports")

        c1, c2 = st.columns(2)

        if excel_file is not None:

            c1.download_button(
                "📥 Export Excel",
                excel_file,
                "Rapport_FCP.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if pdf_file is not None:

            c2.download_button(
                "📄 Export PDF",
                pdf_file,
                "Rapport_Comite.pdf",
                mime="application/pdf"
            )

    # PERFORMANCES

    with tab2:

        st.plotly_chart(
            plot_nav(perf_df),
            width="stretch"
        )

        st.plotly_chart(
            plot_performance(
                perf_df
            ),
            width="stretch"
        )

    # RISQUES

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

    # SENSIBILITE

    with tab4:

        st.plotly_chart(
            plot_sensitivity(
                sensi_df
            ),
            width="stretch"
        )

    # COMITE

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
        "Importer votre fichier Excel"
    )
