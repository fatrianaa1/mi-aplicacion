import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import cufflinks as cf



# Definir tabla de datos:
datos = pd.read_csv("https://gist.githubusercontent.com/fatrianaa1/76c832481a4fdb2e3683c2b232b5476f/raw/data_acciones.csv", 
                    delimiter = "\t")
datos["Fecha"] = pd.to_datetime(datos["Fecha"])
datos = datos[datos["Cantidad"] > 0]
lista_de_acciones = sorted(list(datos["Nemotecnico"].unique()))

# Definir funciones auxiliares:
# Bandas de Bollinger:
def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

# Inicializar la aplicación:
app = dash.Dash(__name__)
server = app.server
app.title= "Valkiria"



# Configurar aplicación
app.layout = html.Div([
    html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("valkiria.png"),
                        id="plotly-image",
                        style={
                            "height": "60px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                    )
                ],
                className="one-third column",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Análisis técnico de acciones de la BVC",
                                style={"margin-bottom": "0px"},
                            ),
                            html.H6(
                                "Escrito en Python por Fabián Triana", style={"margin-top": "0px"}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            ),
            html.Div(
                [
                    html.A(
                        html.Button("Sobre el autor", id="learn-more-button"),
                        href="https://www.linkedin.com/in/fabiantriana/",
                    )
                ],
                className="one-third column",
                id="button",
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"},
    ),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.H4(id="well_text"), 
                                 html.P("Variación")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="gasText"), html.P("Gas")],
                                id="gas",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="oilText"), html.P("Oil")],
                                id="oil",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="waterText"), html.P("Water")],
                                id="water",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="otroText"), html.P("Otra vaina")],
                                id="sector",
                                className="mini_container",)
                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                ],
                id="right-column",
                className="twelve columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Br(),
    html.Div([dcc.Dropdown(
        id= "dropdown",
        options=[{"label": i, "value": i} for i in lista_de_acciones],
        value= "ECOPETROL"
    )], className = 'three columns'),
    html.Br(),
    html.Div([dcc.Graph(id='grafico_principal')], className = "eight columns")
])



# Definir callbacks:

# Actualizar gráfico principal con la acción seleccionada:
@app.callback(Output('grafico_principal', 'figure'),
              [Input('dropdown', 'value')])
def grafica_principal(accion_seleccionada):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    datos_seleccionados = datos_seleccionados.set_index("Fecha")
    
    # Gráfico elaborado con Cufflinks:
    grafico = cf.QuantFig(datos_seleccionados, name = accion_seleccionada)
    
    # Definir colores personalizados con atributo ".theme":
    grafico.theme = {'theme': 'pearl', 'up_color': '#17BECF', 'down_color': 'red'}
    
    # Modificar el atributo "._d" de modo que trabaje con los nombres de
    # las columnas del dataframe y entienda a qué se refiere cada una:
    grafico._d = {'open': 'Apertura', 'high': 'Alto', 'low': 'Bajo', 'close': 'Cierre'}
    
    # Añadir los estudios técnicos:
    grafico.add_volume(column = "Cantidad")
    grafico.add_bollinger_bands(periods = 5)
    
    # Crear el gráfico principal como figura plotly:
    el_grafico_principal = grafico.figure()
    # el_grafico_principal.update_layout(xaxis_rangeslider_visible=False)

    # Devolver el gráfico principal:
    return el_grafico_principal

# Actualizar color de la variación de acuerdo a última variación
# de la acción seleccionada:
@app.callback([Output("well_text", "style"), 
               Output("well_text", "children")], 
              [Input("dropdown", "value")])
def color(accion_seleccionada):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    fecha_mas_reciente = datos_seleccionados["Fecha"].max()
    datos_mas_recientes = datos_seleccionados[datos_seleccionados["Fecha"] == fecha_mas_reciente]
    ultima_variacion = datos_mas_recientes["Variacion"].values[0]
    ultima_variacion_en_numero = float(ultima_variacion.strip("%"))
    if ultima_variacion_en_numero > 0:
        mi_color = "green"
    elif ultima_variacion_en_numero < 0:
        mi_color = "red"
    else:
        mi_color = "darkblue"
    return {"color": mi_color}, ultima_variacion


if __name__ == '__main__':
    app.run_server()
