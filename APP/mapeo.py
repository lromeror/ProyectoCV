import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Datos para los trazados
trace1 = go.Scattermapbox(
    mode="markers+lines",
    lon=[10, 20, 30],
    lat=[10, 20, 30],
    marker={'size': 10}
)

trace2 = go.Scattermapbox(
    mode="markers+lines",
    lon=[-50, -60, 40],
    lat=[30, 10, -20],
    marker={'size': 10}
)

# Crear la figura
fig = go.Figure(data=[trace1, trace2])

# Diseño del gráfico
fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox={
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'zoom': 1
    }
)

# Diseño de la aplicación
app.layout = html.Div([
    dcc.Graph(id='scattermapbox-graph', figure=fig)
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)