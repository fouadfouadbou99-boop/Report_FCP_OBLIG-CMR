import plotly.graph_objects as go
import plotly.express as px


def plot_nav(df):

    fig = go.Figure()

    for col in ["SANADATE_VL", "BONDS_VL", "OBLIG_VL"\]:

        if col in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=col
                )
            )

    return fig


def plot_performance(df):

    fig = go.Figure()

    for col in ["SANADATE_YTD", "BONDS_YTD", "OBLIG_YTD"\]:

        if col in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=col
                )
            )

    return fig


def plot_drawdown(df):

    fig = go.Figure()

    for col in ["SANADATE_VL", "BONDS_VL", "OBLIG_VL"\]:

        if col in df.columns:

            dd = df[col] / df[col].cummax() - 1

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=dd,
                    name=col
                )
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

    return fig


def plot_risk_return(df):

    if (
        "Volatilité" in df.columns
        and "Perf Annualisée" in df.columns
    ):

        return px.scatter(
            df,
            x="Volatilité",
            y="Perf Annualisée",
            text="Fonds"
        )

    return go.Figure()
``
