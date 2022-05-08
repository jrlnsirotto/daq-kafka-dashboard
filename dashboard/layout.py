import sys, os
import dash_daq as daq, dash_bootstrap_components as dbc
from dash import dcc, html

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dashboard import elements as el

layout = dbc.Container(
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
                                                children="DELETE",
                                                style={
                                                    "margin-top": f"10px",
                                                    "margin-left": f"20px",
                                                },
                                            ),
                                            html.Button(
                                                "SUBMIT",
                                                id="delete_measurement",
                                                n_clicks=0,
                                                style={
                                                    "margin-top": f"10px",
                                                    "margin-left": f"10px",
                                                    "width": 80,
                                                },
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6(
                                                children="MEASUREMENTS",
                                                style={
                                                    "margin-top": f"10px",
                                                    "margin-left": f"-20px",
                                                },
                                            ),
                                            html.H2(
                                                children="-",
                                                id="times_measured",
                                                style={"margin-left": f"40px"},
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
                    dbc.Row(
                        [
                            html.H6(
                                "*AFTER DELETING A MEASUREMENT CONSIDER REFRESH YOUR DATABASE",
                                style={
                                    "margin-top": f"20px",
                                    "margin-left": f"10px",
                                },
                            )
                        ],
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
