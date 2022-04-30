import sys, os, httpx, json
import pandas as pd
import dash_renderjson, dash_daq as daq, dash_bootstrap_components as dbc
from dash import dcc, html


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dashboard import elements as el
from data_storage import manipulate_hdf5
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform

# Style dashboard

app = DashProxy(
    prevent_initial_callbacks=True,
    transforms=[MultiplexerTransform()],
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
)


###############################################################
#                           LAYOUT                            #
###############################################################

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    el.textBox(
                                        "DATA VISUALIZER",
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H6(
                                                children="DATETIME FILTER",
                                                style={"margin-top": f"10px"},
                                            ),
                                            html.Div(
                                                id="element_dp", children=el.sample_dp()
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6(
                                                children=" MEASUREMENTS",
                                                style={
                                                    "margin-top": f"10px",
                                                    "margin-left": f"80px",
                                                },
                                            ),
                                            html.H2(
                                                children="-",
                                                id="times_measured",
                                                style={"margin-left": f"130px"},
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dcc.Graph(
                                id="graph_line",
                                figure=el.sample_plot(),
                                style={"width": 700, "height": 400},
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("REFRESH DATABASE"),
                                    html.Button(
                                        "SUBMIT",
                                        id="refresh_database",
                                        n_clicks=0,
                                        style={
                                            "margin-top": f"10px",
                                            "margin-left": f"10px",
                                            "width": 150,
                                        },
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("FIRST MEASUREMENT"),
                                    html.H5(children="-", id="first_measurement"),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("LAST MEASUREMENT"),
                                    html.H5(children="-", id="last_measurement"),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Col(
                [
                    el.textBox("EXPERIMENT CONTROL"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("ACQUISITION"),
                                    html.Button(
                                        "SUBMIT",
                                        id="activate",
                                        n_clicks=0,
                                        style={
                                            "margin-top": f"10px",
                                        },
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("STOP ACQUISITION"),
                                    html.Button(
                                        "SUBMIT",
                                        id="deactivate",
                                        n_clicks=0,
                                        style={
                                            "margin-top": f"10px",
                                        },
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("STATUS"),
                                    daq.Indicator(
                                        id="indicator",
                                        width=60,
                                        height=40,
                                        style={
                                            "margin-top": f"10px",
                                        },
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col([el.textBox("SETTINGS")]),
                            dbc.Col(
                                [
                                    daq.ToggleSwitch(
                                        value=False,
                                        id="toggle",
                                        label="SET NEW",
                                        labelPosition="right",
                                        style={
                                            "margin-top": f"55px",
                                            "margin-left": f"15px",
                                        },
                                    )
                                ],
                            ),
                            dbc.Col([html.Div(id="empty_space")]),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("CURRENT SETTINGS"),
                                    html.Button(
                                        "CHECK",
                                        id="settings_check",
                                        n_clicks=0,
                                        style={
                                            "margin-top": f"10px",
                                        },
                                    ),
                                    html.Div(id="output"),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Div(id="empty_output"),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            dcc.Store(id="store-data", data=[], storage_type="local"),
        ]
    )
)


###############################################################
#                           CALLBACKS                         #
###############################################################


@app.callback(
    [
        Output("store-data", "data"),
        Output("graph_line", "figure"),
        Output("element_dp", "children"),
        Output("first_measurement", "children"),
        Output("last_measurement", "children"),
        Output("times_measured", "children"),
    ],
    Input("refresh_database", "n_clicks"),
)
def refresh_data(n_clicks):
    if n_clicks.numerator >= 1:
        api_out = httpx.get("http://127.0.0.1:8000/dataset/data")

        data = pd.DataFrame(json.loads(api_out.content))

        data = data.explode(["time", "signal"])

        output = (
            data.to_dict("records"),
            el.scatterGraph(data, "time", "signal", "id", "ACQUIRED SIGNAL"),
            el.dropDown(data, "id", "DATETIME FILTER", "drop_down"),
            f"{data['id'].min()[0:19]} BRT",
            f"{data['id'].max()[0:19]} BRT",
            str(len(data["id"].unique())),
        )
        return output


@app.callback(Output("output", "children"), [Input("settings_check", "n_clicks")])
def display_output(n_clicks):
    if n_clicks.numerator >= 1:
        api_output = httpx.get("http://127.0.0.1:8000/items/parameters")
        api_content_json = json.loads(api_output.content)
        return dash_renderjson.DashRenderjson(
            id="input", data=api_content_json, max_depth=-1, invert_theme=True
        )


@app.callback(
    [Output("indicator", "color")],
    [Input("activate", "n_clicks")],
)
def activate(n_clicks):

    if n_clicks.numerator >= 1:
        httpx.get("http://127.0.0.1:8000/items/parameters/start")
        return "#00FF00"


@app.callback(
    [Output("indicator", "color")],
    [Input("deactivate", "n_clicks")],
)
def deactivate(n_clicks):

    if n_clicks.numerator >= 1:
        httpx.get("http://127.0.0.1:8000/items/parameters/finish")
        return "#FF0000"


@app.callback(Output("empty_output", "children"), [Input("toggle", "value")])
def display_output(value):

    if value:

        return [
            html.H6("INPUT SETTINGS"),
            dcc.Input(
                id="fs",
                type="number",
                placeholder="Freq. Sampling [Hz]",
                style={
                    "margin-top": f"10px",
                },
            ),
            dcc.Input(
                id="time",
                type="number",
                placeholder="Duration [s]",
                style={
                    "margin-top": f"10px",
                },
            ),
            dcc.Input(
                id="amplitude",
                type="number",
                placeholder="Amplitude [V]",
                style={
                    "margin-top": f"10px",
                },
            ),
            dcc.Input(
                id="frequency",
                type="number",
                placeholder="Frequency [Hz]",
                style={
                    "margin-top": f"10px",
                },
            ),
            html.H6(
                "*Will affect the next measurements",
                style={
                    "margin-top": f"10px",
                },
            ),
            html.Button(
                "SUBMIT",
                id="submit_settings",
                n_clicks=0,
                style={
                    "margin-top": f"10px",
                },
            ),
        ]


@app.callback(
    Output("submit_settings", "n_clicks"),
    [
        Input("submit_settings", "n_clicks"),
        Input("fs", "value"),
        Input("time", "value"),
        Input("amplitude", "value"),
        Input("frequency", "value"),
    ],
)
def new_settings(n_clicks, fs, time, amplitude, frequency):

    if n_clicks == None:
        pass

    if n_clicks.numerator >= 1:
        new_parameters = {
            "freq_sampling": fs,
            "time_measured": time,
            "senoidal_amplitude": amplitude,
            "senoidal_frequency": frequency,
            "last_updated": str(pd.Timestamp.now()),
            "updated_action": "New settings",
        }
        httpx.post(
            "http://127.0.0.1:8000/items/parameters/modify",
            data=json.dumps(new_parameters),
        )
        return 0


@app.callback(
    [Output("graph_line", "figure")],
    [
        Input("drop_down", "value"),
        Input("store-data", "data"),
        Input("refresh_database", "n_clicks"),
    ],
)
def update_figure(value, data, n_clicks):

    data_df = pd.DataFrame(data)

    df = data_df.explode(["time", "signal"]).copy()

    if (value == None) or (value == "-") or (n_clicks.numerator < 1):
        return el.scatterGraph(el.sample_df(), "x", "y", "id")

    elif value == "DATETIME FILTER" and n_clicks.numerator >= 1:
        return el.scatterGraph(df, "time", "signal", "id")

    else:
        return el.scatterGraph(df[df["id"] == value], "time", "signal", "id")


if __name__ == "__main__":

    app.run_server(debug=True)
