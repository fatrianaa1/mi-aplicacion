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

# Definir variables:
myheading1 = 'Plotly Dash -- multiple tabs'
tabtitle = 'dash tabs'
sourceurl = 'https://dash.plot.ly/dash-core-components/tabs'
githublink = 'https://github.com/austinlasseter/dash-multitab-simple

# Inicializar la aplicación:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title= "Valkiria"


# Configurar aplicación
app.layout = html.Div([
    html.Div([
        html.H2("Mi Aplicación"),
        html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    html.Div([
        dcc.Input(id="stock-input", value="ECOPETROL", type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className="six columns"),

        html.Div([
            html.H3("Market News"),
            generate_html_table()
        ], className="six columns"),

    ],className="row")
])



# Definir callbacks:
@app.callback(Output("graph_close")

beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


if __name__ == '__main__':
    app.run_server()
