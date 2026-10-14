import plotly.express as px

def plot_nav(df):

    fig = px.line(
        df,
        x="Date",
        y=["SANADATE","BONDS","OBLIGATIONS"]
    )

    return fig

def plot_performance(df):

    fig = px.line(
        df
    )

    return fig

def plot_drawdown(df):

    fig = px.area(df)

    return fig

def plot_sensitivity(df):

    fig = px.line(df)

    return fig

def plot_risk_return(df):

    fig = px.scatter(df)

    return fig
