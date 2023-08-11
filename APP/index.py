
import dash
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import pandas as pd
# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.BOOTSTRAP]  
# external_stylesheets = [dbc.themes.SANDSTONE]
from dash import Dash, dcc, html,callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=external_stylesheets) #external_stylesheets=external_stylesheets
server = app.server
# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/Images/logo_espol.png", height="30px"),className="col1_1"),
                        dbc.Col(html.H6("PROYECTO CALCULO VECTORIAL"),style={"color":"white","font-size":"10vw"},className="Titulo "),
                        dbc.Col(html.H6("GRUPO 6"),style={"color":"white","font-size":"10vw"},className="col1")
                    ],
                    align='center',
                    justify='center'

                ),
                className="row_header"
            ),
        ]
    ),
    style={'justifyContent':'space-around'},
    color="dark",
    dark=True,
)
navbar2 = dbc.Row(
            [
                dbc.Col(html.Img(src="assets/Images/logo_espol.png", height="30px",className="col1_1")),
                dbc.Col(html.H6("PROYECTO CALCULO VECTORIAL"),style={"color":"white","font-size":"10vw"},className="col1_1"),
                dbc.Col(html.H6("GRUPO 6"),style={"color":"white","font-size":"10vw"},className="col1_1")
            ],
            align='center',
            justify='space-between',    
            style={'justifyContent':'space-around'},
            className="Header"
)




# embedding the navigation bar
app.layout = html.Div([
    navbar2
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)