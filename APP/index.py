from datetime import datetime
import dash
import dash_bootstrap_components as dbc
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import interp1d
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
    df = pd.read_csv("APP/assets/data/planificacion.csv",sep=",")
except FileNotFoundError:
    df = pd.read_csv("https://raw.githubusercontent.com/lromeror/ProyectoCV/main/APP/assets/data/planificacion.csv",sep=",")
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
                options=sorted(df.NOMBRE.unique().tolist()),style={'margin-bottom': '30px'},
                value=sorted(df.NOMBRE.unique().tolist())[0]
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
                options=sorted(df.NOMBRE.unique().tolist()),style={'margin-bottom': '30px'},
                value=sorted(df.NOMBRE.unique().tolist())[1]
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
    Output('Materiapartida', 'options'),
    Input('Materiallegada', 'value'))
def set_cities_options(selected_materia_lle):
    try:
        l_filtrada = df['NOMBRE'].unique().tolist()
        l_filtrada.remove(selected_materia_lle)
        return [{'label': i, 'value': i} for i in sorted(l_filtrada)]
    except ValueError:
        l_filtrada = df['NOMBRE'].unique().tolist()
        return [{'label': i, 'value': i} for i in sorted(l_filtrada)]    
    
@app.callback(
    [Output('Bloquepartida', 'options')],
    [Output('Bloquepartida', 'value')],
    Input('Materiapartida', 'value'))
def set_bloques_options(selected_materia):
    dff = df[df['NOMBRE']==selected_materia]
    return [{'label': u, 'value': u} for u in sorted(dff['BLOQUE'].unique().tolist())],dff['BLOQUE'].unique()[0]

@app.callback(
    Output('MateriaLlegada', 'options'),
    Input('Materiapartida', 'value'))
def set_cities_options(selected_materia_ini):
    try:
        l_filtrada = df['NOMBRE'].unique().tolist()
        l_filtrada.remove(selected_materia_ini)
        return [{'label': i, 'value': i} for i in sorted(l_filtrada)]
    except ValueError:
        l_filtrada = df['NOMBRE'].unique().tolist()
        return [{'label': i, 'value': i} for i in sorted(l_filtrada)]    
    
@app.callback(
    [Output('BloqueLlegada', 'options')],
    [Output('BloqueLlegada', 'value')],
    Input('MateriaLlegada', 'value'))
def set_bloques_options(selected_materia_lle):
    dff = df[df['NOMBRE']==selected_materia_lle]
    return [{'label': u, 'value': u} for u in sorted(dff['BLOQUE'].unique().tolist())],dff['BLOQUE'].unique()[0]

mapa=html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Mapa de Rutas",className="text-center")),
        ]),
    dbc.Row(dcc.Graph(id="mapa")),
],fluid=True,className=" container mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "50px","border-radius": "10px"})#container
])

resume =html.Div([
    dbc.Container([
        dbc.Row(
            id="resumen"
        )
],fluid=True,className=" container mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "50px","border-radius": "10px"})#container
])

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
    c = 2*math.asin(math.sqrt(a))

    # Distancia en kilómetros
    distance = R * c

    # Convertir a metros
    distance_meters = distance * 1000

    return distance_meters

def generate_random_path(lat1, lon1, lat2, lon2, deviation=0.002):
    # Generar puntos intermedios con una pequeña desviación aleatoria

    df2 = df[df['BLOQUE']!="CENAIM"].copy()
    mid_lat = (lat1 + lat2) / 2 + deviation * np.random.randn()
    mid_lon = (lon1 + lon2) / 2 + deviation * np.random.randn()
    while(max(df2["LATS"])< mid_lat < min(df2["LATS"])):
        mid_lat = (lat1 + lat2) / 2 + deviation * np.random.randn()
    while(max(df2["LONGS"])< mid_lat <min(df2["LONGS"])):
        mid_lon = (lon1 + lon2) / 2 + deviation * np.random.randn()


    return [lat1,mid_lat,lat2],[lon1,mid_lon,lon2]

@app.callback(
    Output('mapa','figure'),
    [Input('Materiapartida', 'value')],
    [Input('Bloquepartida', 'value')],
    [Input('MateriaLlegada', 'value')],
    [Input('BloqueLlegada', 'value')])
def grafica(Materiapartida,Bloquepartida,MateriaLlegada,BloqueLlegada): 
    try:
        lat1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LATS'].values[0]
        lon1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LONGS'].values[0]
        lat2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LATS'].values[0]
        lon2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LONGS'].values[0]
        data = {
            'lon': [lon1, lon2],
            'lat': [lat1, lat2],
            'size': [5, 5],
            'Ubicaciones':[Materiapartida,MateriaLlegada,]
        }
        # Crear gráfico con marcadores
        fig = px.scatter_mapbox(data, 
                                lat='lat', 
                                lon='lon',
                                size='size',
                                color='Ubicaciones',
                                size_max=20,
                                zoom=15,)
        # Añadir líneas
        fig.add_traces(go.Scattermapbox(
            mode="lines",
            lon=[lon1, lon2],
            lat=[lat1, lat2],
            line=dict(width=2, color='Green'),
            name='CAMINO MÁS CORTO',
        ))
        # Número de caminos aleatorios a generar
        dic={0:"Purple",1:"Red",2:"Blue"}
        num_random_paths = 2
        for p in range(num_random_paths):
            path_lat, path_lon = generate_random_path(lat1, lon1, lat2, lon2)
            fig.add_traces(go.Scattermapbox(
        mode="lines",
        lon=path_lon,
        lat=path_lat,
        line=dict(width=2, color=dic[p]),
        name='Camino Aleatorio',
        ))

        # Actualizar el estilo del mapa y centrar
        fig.update_layout(mapbox_style="open-street-map", 
                        mapbox={'center': {'lat':-2.14730,'lon': -79.9630}})
        # Actualizar márgenes
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    except : 
        current_time = datetime.now().time()
        date = datetime.now().date
        with open('APP/assets/data/errores.txt', 'a') as archivo:
            archivo.write(f"Error {date} hora: {current_time}\n")

@app.callback(
    Output('resumen','children'),
    [Input('Materiapartida', 'value')],
    [Input('Bloquepartida', 'value')],
    [Input('MateriaLlegada', 'value')],
    [Input('BloqueLlegada', 'value')])
def mostrar_resumen(Materiapartida,Bloquepartida,MateriaLlegada,BloqueLlegada):
    if BloqueLlegada==Bloquepartida :
        return dbc.Col(html.H4(f"Se punto de llegada se encuentra en el mismo bloque {BloqueLlegada}"),className="text-center")
    else:
        try:
            lat1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LATS'].values[0]
            lon1=df[(df['NOMBRE']==Materiapartida) & (df['BLOQUE']==Bloquepartida)]['LONGS'].values[0]
            lat2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LATS'].values[0]
            lon2=df[(df['NOMBRE']==MateriaLlegada) & (df['BLOQUE']==BloqueLlegada)]['LONGS'].values[0]
            distancia = haversine_distance(lat1,lon1,lat2,lon2)
            return dbc.Col(html.H4(f"La distancia más corta, desde el bloque {Bloquepartida}({Materiapartida.title()}) hasta el bloque {BloqueLlegada}({MateriaLlegada.title()}) es {round(distancia,2)} metros"),className="text-center")
        except:
            current_time = datetime.now().time()
            date = datetime.now().date
            with open('APP/assets/data/errores.txt', 'a') as archivo:
                archivo.write(f"Error {date} hora: {current_time}\n")
integrantes =html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(html.H6('ANGELO ZURITA - LUIS ROMERO - GABRIEL DELGADO - DAVID SUMBA - PARALELO 6 - ©2023',className="text-center centrado"))
        )
],fluid=True,className=" container mt-4 g-0",style={"background-color": "#f2f2f2", "padding": "10px","border-radius": "10px",'text-align':'center'})#container
])
app.layout = html.Div([
    navbar2,tituloProyecto,menuHorario,resume, mapa,integrantes
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',port=8020 ,debug=True)

