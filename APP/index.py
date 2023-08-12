
import dash
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
external_stylesheets = [dbc.themes.BOOTSTRAP]  
from dash import Dash, dcc, html,callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# bootstrap theme
# https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.SANDSTONE]


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
#df = pd.read_csv(os.path.join(DATAS_DIR,'planificacion.csv'),sep=",")

try:
    df = pd.read_excel("APP/assets/data/planificacion.xlsx",sheet_name="Sheet1")
except FileNotFoundError:
    df = pd.read_excel("https://raw.githubusercontent.com/lromeror/ProyectoCV/main/APP/assets/data/planificacion.xlsx",sheet_name="Sheet1")
    #ahí que estar actualizando

distancia=0
menuHorario=html.Div([
    dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H3('Ubicaciones de Partida'),
            html.H6('Materia:'),
            dcc.Dropdown(
                
                id='Materiapartida',
                options=df.NOMBRE,style={'margin-bottom': '30px'},
                value=df.NOMBRE.unique().tolist()[0]
            ),html.H6('Bloque:'),
            dcc.Dropdown(
                id='Bloquepartida',
                options=df.BLOQUE,style={'margin-bottom': '50px'},
                value=df.BLOQUE.unique().tolist()[0]
            ),
        ], width=5, style={'padding': '20px', 'background-color': '#889694 ',"border-radius": "5px"}),
        dbc.Col([html.H1(" ")],width=2),
        # Contenido principal
        dbc.Col([
            html.H3('Ubicaciones de Llegada'),
            html.H6('Materia:'),
            dcc.Dropdown(
                id='MateriaLlegada',
                options=df.NOMBRE,style={'margin-bottom': '30px'},
                value=df.NOMBRE.unique().tolist()[1]
            ),html.H6('Bloque:'),
            dcc.Dropdown(
                id='BloqueLlegada',
                options=df.BLOQUE,style={'margin-bottom': '50px'},
                value=df.BLOQUE.unique().tolist()[1]
            ),
        ], width=5, style={'padding': '20px', 'background-color': '#889694 ',"border-radius": "5px"})
    ]),
],fluid=True,className=" container mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "50px","border-radius": "10px"})#container
])

@app.callback(
    Output('Bloquepartida', 'options'),
    Input('Materiapartida', 'value'))
def set_bloques_options(selected_materia):
     dff = df[df['NOMBRE']==selected_materia]
     return [{'label': i, 'value': i} for i in dff['BLOQUE'].unique()]

@app.callback(
    Output('MateriaLlegada', 'options'),
    Input('Materiapartida', 'value'))
def set_cities_options(selected_materia_ini):
    try:
        l_filtrada = df['NOMBRE'].unique().tolist()
        l_filtrada.remove(selected_materia_ini)
        return [{'label': i, 'value': i} for i in l_filtrada]
    except ValueError:
        l_filtrada = df['NOMBRE'].unique().tolist()
        return [{'label': i, 'value': i} for i in l_filtrada]    
    
@app.callback(
    Output('Bloquellegada', 'options'),
    Input('Materiallegada', 'value'))
def set_bloques_options(selected_materia_lle):
     dff = df[df['NOMBRE']==selected_materia_lle]
     return [{'label': i, 'value': i} for i in dff['BLOQUE'].unique()]

mapa=html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Mapa de Rutas",className="text-center")),
        ]),
    dbc.Row(dcc.Graph(id="mapa")),
],fluid=True,className=" container mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "50px","border-radius": "10px"})#container
])

@app.callback(
    Output('mapa','figure'),
    [Input('Materiapartida', 'value')],
    [Input('Bloquepartida', 'value')],
    [Input('MateriaLlegada', 'value')],
    [Input('BloqueLlegada', 'value')])
def grafica(Materiapartida,Bloquepartida,MateriaLlegada,BloqueLlegada):
   # global distancia
    lat1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LATS'].values[0]
    lon1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LONGS'].values[0]
    lat2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LATS'].values[0]
    lon2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LONGS'].values[0]
    print(type(lat1))
    print(type(lat2))
    print(type(lon1))
    print(type(lon2))
    fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [lon1, lon2],
    lat = [lat1, lat2],
    marker = {'size': 10}))
    fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1},mapbox_style="open-street-map")

    #distancia= haversine_distance(lat1,lon1,lat2,lon2)

    return fig

#Funcion para calcular la distancia entre dos puntos
def haversine_distance(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia de coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula del haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c

    # Convertir a metros
    distance_meters = distance * 1000

    return distance_meters


us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
us_cities = us_cities.query("State in ['New York', 'Ohio']")
grafica=html.Div([
    dcc.Graph(id="city-map"),
])


@app.callback(
    Output("city-map", "figure"),
    Input("city-map", "relayoutData")
)
def update_map(relayoutData):
    # Crear la figura del mapa
    fig = px.line_mapbox(us_cities, lat="lat", lon="lon", color="State", zoom=3, height=800)
    
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat=41,
                    margin={"r": 0, "t": 0, "l": 0, "b": 0})
    
    return fig








app.layout = html.Div([
    navbar2,tituloProyecto,menuHorario,mapa
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',port=8020 ,debug=True)

