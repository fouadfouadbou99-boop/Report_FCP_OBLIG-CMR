import plotly.express as px

def nav_chart(df):

    fig = px.line(
        df,
        x="Date",
        y="VL",
        title="Evolution VL"
    )

    return fig
