import sys, os, httpx, json
import pandas as pd
import dash_renderjson
from dash import dcc, html

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dashboard import elements as el

from dash_extensions.enrich import Output, Input, State


def register_callback(app):
    @app.callback(
        [
            Output("store-data", "data"),
            Output("graph_line", "figure"),
            Output("element_dp", "children"),
            Output("first_measurement", "children"),
            Output("last_measurement", "children"),
            Output("times_measured", "children"),
        ],
        [Input("refresh_database", "n_clicks")],
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
            api_output = httpx.get("http://127.0.0.1:8000/daq/parameters")
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
            httpx.get("http://127.0.0.1:8000/daq/start")
            return "#00FF00"

    @app.callback(
        [Output("indicator", "color")],
        [Input("deactivate", "n_clicks")],
    )
    def deactivate(n_clicks):

        if n_clicks.numerator >= 1:
            httpx.get("http://127.0.0.1:8000/daq/finish")
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
                "http://127.0.0.1:8000/daq/parameters/modify",
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

    @app.callback(
        [
            Output("delete_measurement", "n_clicks"),
        ],
        [Input("delete_measurement", "n_clicks"), Input("drop_down", "value")],
    )
    def delete_measurement(n_clicks, value):
        if n_clicks.numerator == 0:
            return 0

        if n_clicks.numerator >= 1:
            new_parameters = {"measurement": value}
            httpx.post(
                "http://127.0.0.1:8000/dataset/data/delete",
                data=json.dumps(new_parameters),
            )

            return 0
