import sys, os
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dashboard.layout import layout
from dashboard.callbacks import register_callback

# Style dashboard

app = DashProxy(
    prevent_initial_callbacks=True,
    transforms=[MultiplexerTransform()],
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
)

app.layout = layout
register_callback(app)

if __name__ == "__main__":

    app.run_server(debug=True)
