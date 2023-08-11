
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
import os
import plotly.express as px
import pandas as pd
# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.BOOTSTRAP]  
# external_stylesheets = [dbc.themes.SANDSTONE]
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server


header = html.H4("ZZZZZZZZZZZ")

app.layout = dbc.Container([header])




if __name__ == '__main__':
    app.run_server(debug=True)