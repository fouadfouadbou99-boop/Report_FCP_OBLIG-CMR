import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def plot_nav(df):

    fig = go.Figure()

    if "SANADATE_VL" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["SANADATE_VL"],
                name="SANADATE"
            )
        )

    if "BONDS_VL" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["BONDS_VL"],
                name="BONDS"
            )
        )

    if "OBLIG_VL" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["OBLIG_VL"],
                name="OBLIGATIONS"
            )
        )

    fig.update_layout(
        title="Evolution des VL"
    )

    return fig


def plot_performance(df):

    fig = go.Figure()

    if "SANADATE_YTD" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["SANADATE_YTD"],
                name="SANADATE"
            )
        )

    if "BONDS_YTD" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["BONDS_YTD"],
                name="BONDS"
            )
        )

    if "OBLIG_YTD" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["OBLIG_YTD"],
                name="OBLIGATIONS"
            )
        )

    fig.update_layout(
        title="Evolution des performances"
    )

    return fig


def plot_drawdown(df):

    fig = go.Figure()

    fonds = [
        "SANADATE_VL",
        "BONDS_VL",
        "OBLIG_VL"
    ]

    for col in fonds:

        if col in df.columns:

            nav = df[col]

            drawdown = nav / nav.cummax() - 1

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=drawdown,
                    name=col.replace("_VL", "")
                )
            )

    fig.update_layout(
        title="Maximum Drawdown"
    )

    return fig


def plot_sensitivity(df):

    fig = go.Figure()

    for col in ["SANADATE", "BONDS", "OBLIGATIONS"\]:

        if col in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=col
                )
            )

    fig.update_layout(
        title="Evolution des sensibilités"
    )

    return fig


def plot_risk_return(df):

    if "Volatilité" not in df.columns:
        return px.scatter()

    if "Perf Annualisée" not in df.columns:
        return px.scatter()

    fig = px.scatter(
        df,
        x="Volatilité",
        y="Perf Annualisée",
        text="Fonds"
    )

    fig.update_layout(
        title="Risque / Rendement"
    )

    return fig
