
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
                        dbc.Col(html.Img(src="assets/Images/logo_espol.png", height="460px"),className="col1_1"),
                        dbc.Col(html.H6("PROYECTO CALCULO VECTORIAL"),style={"color":"white","font-size":"20vw"},className="Titulo"),
                        dbc.Col(html.H6("GRUPO 6"),style={"color":"white","font-size":"10vw"},className="col1")
                    ],
                    align='center',
                    justify='center'

                ),
                className="row_header g-0"
            ),
        ]
    ),
    style={'justifyContent':'space-around'},
    color="dark",
    dark=True,
)
navbar2 = dbc.Row(
            [
                dbc.Col(html.Img(src="assets/images/logo_espol.png", height="41px",className="col1_1")),
                dbc.Col(html.H5("PROYECTO CALCULO VECTORIAL"),style={"color":"white","font-size":"10vw"},className="col1_1"),
                dbc.Col(html.H5("GRUPO 6"),style={"color":"white","font-size":"10vw"},className="col1_1")
            ],
            align='center',
            justify='space-between',    
            style={'justifyContent':'space-around'},
            className="Header g-0"
)
tituloProyecto=dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("OPTIMIZACION DE RUTAS EN LAS AULAS CLASES"),className="col1_1"),
    ])
])
#Dataset de planificacion de clases

PAGES_DIR = os.path.dirname(__file__)
APP_DIR = os.path.relpath(os.path.dirname(PAGES_DIR))
ASSETS_DIR = os.path.relpath(os.path.join(APP_DIR,'assets'))
DATAS_DIR = os.path.relpath(os.path.join(ASSETS_DIR,'data'))
#df = pd.read_excel(os.path.join(DATAS_DIR,'planificacion.csv'),sheet_name="Hoja1")
df = pd.read_csv(os.path.join(DATAS_DIR,'planificacion.csv'),sep=",")
bosy=html.Div([
    dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H2('Ubicaciones'),
            html.H6('Origen:'),
            dcc.Dropdown(
                
                id='dropdown1',
                options=[
                    {'label': 'Opción 1', 'value': 'opt1'},
                    {'label': 'Opción 2', 'value': 'opt2'},
                    {'label': 'Opción 3', 'value': 'opt3'}
                ],style={'margin-bottom': '50px'},
                value='opt1'
            ),html.H6('Llegada:'),
            dcc.Dropdown(
                
                id='dropdown2',
                options=[
                    {'label': 'A', 'value': 'A'},
                    {'label': 'B', 'value': 'B'},
                    {'label': 'C', 'value': 'C'}
                ],
                value='A'
            ),
        ], width=2, style={'padding': '20px', 'background-color': '#889694 ',"border-radius": "5px"}),

        # Contenido principal
        dbc.Col([
            html.H1('Aqui va el mapa'),
        ], width=9, style={'padding': '20px'}),
    ]),
],fluid=True,className=" mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "50px","border-radius": "10px"})#container
])

#map = dbc.Container([
#    html.Iframe(src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3987.0205291828083!2d-79.96704509721975!3d-2.1458240017673655!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x902d72f925e5bfdb%3A0x327cdb9f7f4ba3b2!2sEscuela%20Superior%20Polit%C3%A9cnica%20del%20Litoral%20(ESPOL)!5e0!3m2!1ses!2sec!4v1691779963691!5m2!1ses!2sec" ,width="600" ,height="450")
#])


# embedding the navigation bar
tituloProyecto=dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("OPTIMIZACION DE RUTAS EN LAS AULAS CLASES"),className="col1_1"),
    ])

])
app.layout = html.Div([
    navbar2,tituloProyecto,bosy
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',port=8020 ,debug=True)

