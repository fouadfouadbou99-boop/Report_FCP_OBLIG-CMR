import plotly.express as px
import plotly.graph_objects as go

def plot_nav(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SANADATE_VL"],
            name="SANADATE"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["BONDS_VL"],
            name="BONDS"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
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

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SANADATE_YTD"],
            name="SANADATE"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["BONDS_YTD"],
            name="BONDS"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["OBLIG_YTD"],
            name="OBLIGATIONS"
        )
    )

    return fig
