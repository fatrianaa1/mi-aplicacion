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
                            html.H5(
                                "Otra cosa", style={"margin-top": "0px"}
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
                                [html.H6(id="well_text"), html.P("No. of Wells")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="gasText"), html.P("Gas")],
                                id="gas",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="oilText"), html.P("Oil")],
                                id="oil",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="waterText"), html.P("Water")],
                                id="water",
                                className="mini_container",
                            ),
                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                ],
                id="right-column",
                className="eight columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Div(
        [
            html.Div(
                [
                    html.H4("Capitalización bursátil"), 
                    html.H2("6 Billones"
                           )
                ], 
                className = "six columns"
            ), 
            html.Div(
                [
                    html.H4("Variación"), 
                    html.H2(id = "la_variación", children = ["-3%"]
                           )
                ], 
                className = "six columns"
            )
        ], 
        className = "twelve columns"),
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

@app.callback(Output("la_variación", "style"), 
              [Input("dropdown", "value")])
def color(accion_seleccionada):
    if accion_seleccionada == "ECOPETROL":
        mi_color = "red" 
    else:
        mi_color = "blue"
    return {"color": mi_color}

if __name__ == '__main__':
    app.run_server()
