import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np



# Definir tabla de datos:
datos = pd.read_csv("https://gist.githubusercontent.com/fatrianaa1/76c832481a4fdb2e3683c2b232b5476f/raw/data_acciones.csv", delimiter = "\t")
datos["Fecha"] = pd.to_datetime(datos["fecha"], format = "%d/%m/%Y %H:%M:%S")
datos = datos[datos["Cantidad"] > 0]
lista_de_acciones = list(datos['Nemotecnico'].value_counts().sort_index().index)



# Inicializar la aplicación:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title= "Valkiria"



# Configurar aplicación
app.layout = html.Div([
    html.Div(
        [
            html.Div(
                [
                    html.H2(
                        'Análisis técnico de acciones', 
                        style = {'margin-bottom': '0px'},
                    ), 
                    html.H5(
                        'Otra cosa', style = {'margin-top':'0px'}
                    ),
                ]
            )
        ], 
        className = 'one-half column',
    ),
    html.H3('Análisis técnico de acciones de la BVC'),
    html.Div([dcc.Dropdown(
        id= "dropdown",
        options=[{"label": i, "value": i} for i in lista_de_acciones],
        value= "ECOPETROL"
    )], className = 'three columns'),
    html.Br(),
    dcc.Graph(id='grafico_principal')
])



# Definir callbacks:
@app.callback(Output('grafico_principal', 'figure'),
              [Input('dropdown', 'value')])
def grafica_principal(accion_seleccionada):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    el_grafico_principal = go.Candlestick(x = datos_seleccionados["Fecha"], 
                                          open = datos_seleccionados["Precio Medio"], 
                                          high = datos_seleccionados["Precio Mayor"],
                                          low = datos_seleccionados["Precio Menor"], 
                                          close = datos_seleccionados["Precio Cierre"])
    figura_principal = go.Figure(data = [el_grafico_principal])
    return figura_principal

if __name__ == '__main__':
    app.run_server()
