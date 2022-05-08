from dash import html, dcc, Dash
import plotly.express as px
import pandas as pd


def textBox(title, subtitle=None, mgleft=0, mgright=0, mgtop=50, mgbottom=50):

    return html.Div(
        children=[
            html.H1(children=title, style={"margin-top": f"{mgtop}px"}),
            html.Div(
                children=subtitle,
                style={
                    "margin-left": f"{mgleft}px",
                    "margin-right": f"{mgright}px",
                    "margin-top": f"{mgtop}px",
                    "margin-bottom": f"{mgbottom}px",
                },
            ),
        ]
    )


def generateTable(dataframe, max_rows=10):
    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
                    )
                    for i in range(min(len(dataframe), max_rows))
                ]
            ),
        ],
        style={"transform": "scale(1)"},
    )


def scatterGraph(
    df, colX, colY, colors=None, title=None, xlabel="Time [s]", ylabel="Amplitude [V]"
):
    if colors == None:
        fig = px.line(data_frame=df, x=df[colX], y=df[colY])
    else:
        fig = px.line(data_frame=df, x=df[colX], y=df[colY], color=df[colors])

    fig.update_layout(
        title=title, xaxis_title=xlabel, yaxis_title=ylabel, legend_title="Legend"
    )
    fig.update_layout(showlegend=False)

    return fig


def pieGraph(df, colX, colY, title="Give me a title"):
    fig = px.pie(values=list(df[colX]), names=list(df[colY]))

    fig.update_layout(title=title, legend_title="Legend")
    return fig


def dropDown(df, col, name, idName):

    return dcc.Dropdown(
        df[col].unique(),
        name,
        id=idName,
        style={"margin-bottom": f"50px", "width": 300, "height": 55},
    )


def sample_df():
    return pd.DataFrame({"x": [0, 10], "y": [0, 0], "id": ["-", "-"]})


def sample_plot():
    df = sample_df()
    return px.line(data_frame=df, x=df["x"], y=df["y"])


def sample_dp():
    df = sample_df()
    return dropDown(df, "id", "DATETIME FILTER", "drop_down")
