import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import cufflinks as cf
from pandas.tseries.offsets import DateOffset



# Definir tabla de datos:
datos = pd.read_csv("https://gist.githubusercontent.com/fatrianaa1/76c832481a4fdb2e3683c2b232b5476f/raw/data_acciones.csv", 
                    delimiter = "\t")
datos["Fecha"] = pd.to_datetime(datos["Fecha"])
datos = datos[datos["Cantidad"] > 0]
lista_de_acciones = sorted(list(datos["Nemotecnico"].unique()))


# Definición de sectores:
sectores = {"BCOLOMBIA": "Financiero", 
            "BOGOTA": "Financiero", 
            "BVC": "Financiero", 
            "CELSIA": "Energía", 
            "CEMARGOS": "Industrial", 
            "CLH": "Industrial", 
            "CNEC": "Petróleo", 
            "CONCONCRET": "Construcción", 
            "CORFICOLCF": "Holdings", 
            "ECOPETROL": "Petróleo", 
            "ETB": "Telecomunicaciones", 
            "EXITO": "Retail", 
            "GEB": "Energía", 
            "GRUPOARGOS": "Holdings", 
            "GRUPOAVAL": "Holdings", 
            "GRUPOSURA": "Holdings", 
            "ISA": "Energía", 
            "NUTRESA": "Alimentos", 
            "PFAVAL": "Holdings", 
            "PFBCOLOM": "Financiero", 
            "PFCEMARGOS": "Industrial", 
            "PFDAVVNDA": "Financiero", 
            "PFGRUPOARG": "Holdings", 
            "PFGRUPSURA": "Holdings"}

# Información de dividendo anual para cálcuo de Yield:
dividendos = {"BCOLOMBIA": 1638, 
              "BOGOTA": 4032, 
              "BVC": 418, 
              "CELSIA": 292, 
              "CEMARGOS": 251, 
              "CLH": 0, 
              "CNEC": 0, 
              "CONCONCRET": 0, 
              "CORFICOLCF": 2640, 
              "ECOPETROL": 180, 
              "ETB": 0, 
              "EXITO": 2438, 
              "GEB": 140, 
              "GRUPOARGOS": 376, 
              "GRUPOAVAL": 60, 
              "GRUPOSURA": 634, 
              "ISA": 675, 
              "NUTRESA": 649, 
              "PFAVAL": 60, 
              "PFBCOLOM": 1638, 
              "PFCEMARGOS": 251, 
              "PFDAVVNDA": 926, 
              "PFGRUPOARG": 376, 
              "PFGRUPSURA": 634}

# Acciones en circulación para cálculo de capitalización:
# PFDAVIVIENDA corresponde a la SUMA del número de acciones preferenciales Y ORDINARIAS
# CORFICOLCF corresponde a la SUMA del número de acciones preferenciales y ordinarias

numero_acciones = {"BCOLOMBIA": 509704584, 
                   "BOGOTA": 331280555, 
                   "BVC": 60513469, 
                   "CELSIA": 1069972554, 
                   "CEMARGOS": 1151672310, 
                   "CLH": 578278342, 
                   "CNEC": 177623000, 
                   "CONCONCRET": 1134254939, 
                   "CORFICOLCF": 324011008, 
                   "ECOPETROL": 41116694690, 
                   "ETB": 3550553412, 
                   "EXITO": 447604316, 
                   "GEB": 9181177017, 
                   "GRUPOARGOS": 645400000, 
                   "GRUPOAVAL": 15137789974, 
                   "GRUPOSURA": 469037260, 
                   "ISA": 1107677894, 
                   "NUTRESA": 460123458, 
                   "PFAVAL": 7143227185, 
                   "PFBCOLOM": 452122416, 
                   "PFCEMARGOS": 209197850, 
                   "PFDAVVNDA": 451670413, 
                   "PFGRUPOARG": 211827180, 
                   "PFGRUPSURA": 112940288} 

# Especificar qué empresas tienen acciones ordinarias
# y acciones preferenciales para calcular la capitalización
# con los precios de ambas especies:
acciones_preferenciales_y_ordinarias = ["BCOLOMBIA", "PFBCOLOM", 
                                        "CEMARGOS", "PFCEMARGOS", 
                                        "GRUPOARGOS", "PFGRUPOARG", 
                                        "GRUPOAVAL", "PFAVAL", 
                                        "GRUPOSURA", "PFGRUPSURA"]

# Diccionario con la acción ordinaria (primera posición) y
# la acción preferencial (segunda posición) para los emmisores
# señalados anteriormente:

Bancolombia = ["BCOLOMBIA", "PFBCOLOM"]
Cemargos = ["CEMARGOS", "PFCEMARGOS"]
Grupo_Argos = ["GRUPOARGOS", "PFGRUPOARG"]
Grupo_Aval = ["GRUPOAVAL", "PFAVAL"]
Grupo_Sura = ["GRUPOSURA", "PFGRUPSURA"]

diccionario_ordinarias_preferenciales = {"BCOLOMBIA": Bancolombia, 
                                         "PFBCOLOM": Bancolombia, 
                                         "CEMARGOS": Cemargos, 
                                         "PFCEMARGOS": Cemargos, 
                                         "GRUPOARGOS": Grupo_Argos, 
                                         "PFGRUPOARG": Grupo_Argos, 
                                         "GRUPOAVAL": Grupo_Aval, 
                                         "PFAVAL": Grupo_Aval, 
                                         "GRUPOSURA": Grupo_Sura, 
                                         "PFGRUPSURA": Grupo_Sura}

# Listado de emisores (se emplea para la actualización de la tabla de
# resumen básico)

emisores = {"BCOLOMBIA": "Bancolombia S.A", 
            "BOGOTA": "Banco de Bogotá S.A", 
            "BVC": "Bolsa de Valores de Colombia S.A", 
            "CELSIA": "Celsia S.A E.S.P", 
            "CEMARGOS": "Cementos Argos S.A", 
            "CLH": "Cemex Latam Holdings S.A", 
            "CNEC": "Canacol Energy Ltd", 
            "CONCONCRET": "Constructora Conconcreto S.A", 
            "CORFICOLCF": "Corporación Financiera Colombiana", 
            "ECOPETROL": "Ecopetrol S.A", 
            "ETB": "Empresa de Telecomunicaciones de Bogotá S.A E.S.P", 
            "EXITO": "Almacenes Éxito S.A", 
            "GEB": "Grupo Energía Bogotá S.A E.S.P", 
            "GRUPOARGOS": "Grupo Argos S.A", 
            "GRUPOAVAL": "Grupo Aval Acciones y Valores S.A", 
            "GRUPOSURA": "Grupo de Inversiones Suramericana S.A", 
            "ISA": "Interconexión Eléctrica S.A", 
            "NUTRESA": "Grupo Nutresa S.A", 
            "PFAVAL": "Grupo Aval Acciones y Valores S.A", 
            "PFBCOLOM": "Bancolombia S.A", 
            "PFCEMARGOS": "Cementos Argos S.A", 
            "PFDAVVNDA": "Banco Davivienda S.A", 
            "PFGRUPOARG": "Grupo Argos S.A", 
            "PFGRUPSURA": "Grupo de Inversiones Suramericana S.A"} 

# Lista de indicdores técnicos:
lista_indicadores_superiores = ["Bollinger Bands", "EMA", "Parabolic SAR"]
lista_indicadores_inferiores = ["MACD", "RSI"]


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
                                [html.H4(id="well_text"), html.P("Variación")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="gasText"), html.P("Último Cierre")],
                                id="gas",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="oilText"), html.P("Capitalización")],
                                id="oil",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="waterText"), html.P("Yield")],
                                id="water",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H4(id="TextoSector"), html.P("Sector")],
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
    html.Div([html.P("Seleccione una acción:", className="control_label"),
        dcc.Dropdown(
        id= "dropdown",
        options=[{"label": i, "value": i} for i in lista_de_acciones],
        value= "ECOPETROL"),
              html.Br(),
              html.P("Seleccione indicadores superiores:", className="control_label"),
              dcc.Checklist(
                  id = "checklist_superiores", 
                  options =[{"label": i, "value": i} for i in lista_indicadores_superiores], 
                  value = ["Bollinger Bands"]), 
              html.P("Seleccione indicadores inferiores:", className="control_label"), 
              dcc.Checklist(
                  id= "checklist_inferiores", 
                  options = [{"label": i, "value": i} for i in lista_indicadores_inferiores], 
                  value = ["MACD"])], 
             className = 'three columns'),
    html.Br(),
    html.Div([dcc.Graph(id='grafico_principal')], className = "six columns"), 
    html.Div([html.H6("Información"), 
              dash_table.DataTable(id = "tabla_resumen", 
                                   data = [], 
                                   columns = [{"name": ["Resumen básico", "Dato"], "id": "Dato"}, 
                                              {"name": ["Resumen básico", "Valor"], "id": "Valor"}], 
                                   style_cell={'fontSize':13, 'fontFamily':'sans-serif', 'textAlign': 'left'}, 
                                   merge_duplicate_headers = True,
                                   style_as_list_view=True, 
                                   style_header = {'fontWeight': 'bold'}, 
                                   style_data = {'whiteSpace': 'normal', 'height': 'auto'})], 
             className = "three columns")
])



# Definir callbacks:

# Actualizar gráfico principal con la acción seleccionada:
@app.callback(Output('grafico_principal', 'figure'),
              [Input('dropdown', 'value'), 
               Input('checklist_superiores', 'value'), 
               Input('checklist_inferiores', 'value')])
def grafica_principal(accion_seleccionada, indicadores_superiores_seleccionados, indicadores_inferiores_seleccionados):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    fecha_mas_reciente = datos_seleccionados["Fecha"].max()
    periodo = 6
    fecha_de_referencia = fecha_mas_reciente-DateOffset(months = periodo)
    datos_seleccionados = datos_seleccionados[datos_seleccionados["Fecha"]>= fecha_de_referencia]
    datos_seleccionados = datos_seleccionados.set_index("Fecha")
    
    # Gráfico elaborado con Cufflinks:
    grafico = cf.QuantFig(datos_seleccionados, 
                          name = accion_seleccionada, legend = "bottom")
    
    # Definir colores personalizados con atributo ".theme":
    grafico.theme = {'theme': 'pearl', 'up_color': '#008000', 'down_color': '#a52a2a'}
    
    # Modificar el atributo "._d" de modo que trabaje con los nombres de
    # las columnas del dataframe y entienda a qué se refiere cada una:
    grafico._d = {'open': 'Apertura', 'high': 'Alto', 'low': 'Bajo', 'close': 'Cierre'}
    
    # Añadir volumen:
    grafico.add_volume(column = "Cantidad")
    
    # Variable ficticia:
    a = 0
    
    # Añadir los estudios técnicos superiores:

    if "Bollinger Bands" in indicadores_superiores_seleccionados: 
        grafico.add_bollinger_bands(periods = 5, name = "BOLL")
    else:
        a = 1
    
    if "EMA" in indicadores_superiores_seleccionados:
        grafico.add_ema()
    else:
        a = 1
        
    if "Parabolic SAR" in indicadores_superiores_seleccionados:
        grafico.add_ptps()
    else:
        a = 1

    # Añadir los estudios técnicos inferiores:
    if "MACD" in indicadores_inferiores_seleccionados:
        grafico.add_macd(name = "MACD")
    else:
        a = 1
        
    if "RSI" in indicadores_inferiores_seleccionados:
        grafico.add_rsi()
    else:
        a = 1
    
    # Crear el gráfico principal como figura plotly:
    # Eliminar la leyenda:
    grafico.data["showlegend"] = False
    el_grafico_principal = grafico.figure()
    el_grafico_principal.update_layout(showlegend=False)
    # el_grafico_principal.update_layout(xaxis_rangeslider_visible=False)

    # Devolver el gráfico principal:
    return el_grafico_principal

# Actualizar color de la variación de acuerdo a última variación, 
# del último precio, del sector y del yield
# de la acción seleccionada:
@app.callback([Output("well_text", "style"), 
               Output("well_text", "children"), 
               Output("gasText", "children"),
               Output("oilText", "children"),
               Output("waterText", "children"),
               Output("TextoSector", "children")],              
              [Input("dropdown", "value")])
def actualizacion_datos(accion_seleccionada):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    fecha_mas_reciente = datos_seleccionados["Fecha"].max()
    datos_mas_recientes = datos_seleccionados[datos_seleccionados["Fecha"] == fecha_mas_reciente]
    el_sector = sectores[accion_seleccionada]
    ultimo_precio = datos_mas_recientes["Cierre"].values[0]
    el_yield = str(format(round((dividendos[accion_seleccionada]/ultimo_precio)*100,2), '.2f'))+"%"
    la_capitalizacion = "0B"
    if accion_seleccionada in acciones_preferenciales_y_ordinarias:
        ordinaria = diccionario_ordinarias_preferenciales[accion_seleccionada][0]
        preferencial = diccionario_ordinarias_preferenciales[accion_seleccionada][1]
        # Precio de la ordinaria:
        datos_ordinaria = datos[datos["Nemotecnico"] == ordinaria]
        fecha_mas_reciente_ordinaria = datos_ordinaria["Fecha"].max()
        precio_ordinaria = datos_ordinaria[datos_ordinaria["Fecha"] == fecha_mas_reciente_ordinaria]["Cierre"].values[0]
            
        # Precio de la preferencial:
        datos_preferencial = datos[datos["Nemotecnico"] == preferencial]
        fecha_mas_reciente_preferencial = datos_preferencial["Fecha"].max()
        precio_preferencial = datos_preferencial[datos_preferencial["Fecha"] == fecha_mas_reciente_preferencial]["Cierre"].values[0]
            
        # Capitalización de la empresa:
        la_capitalizacion = ((precio_ordinaria*numero_acciones[ordinaria])+(precio_preferencial*numero_acciones[preferencial]))/1000000000000
        la_capitalizacion = str(format(la_capitalizacion, '.2f'))+"B"
    else:
        la_capitalizacion = (ultimo_precio*numero_acciones[accion_seleccionada])/1000000000000
        la_capitalizacion = str(format(la_capitalizacion, '.2f'))+"B"
                    
    ultimo_precio = "$"+str(ultimo_precio)
    ultima_variacion = datos_mas_recientes["Variacion"].values[0]
    ultima_variacion_en_numero = float(ultima_variacion.strip("%"))
    if ultima_variacion_en_numero > 0:
        mi_color = "green"
    elif ultima_variacion_en_numero < 0:
        mi_color = "red"
    else:
        mi_color = "darkblue"
    return {"color": mi_color}, ultima_variacion, ultimo_precio, la_capitalizacion, el_yield, el_sector

# Actualización de tabla de resumen básico:
@app.callback([Output("tabla_resumen", "data"), 
               Output("tabla_resumen", "columns")], 
              [Input("dropdown", "value")])
def tabla_de_resumen(accion_seleccionada):
    indicadores = ["Emisor:", "En circulación:"]
    datos_de_la_tabla = [emisores[accion_seleccionada], 
                         str(format(numero_acciones[accion_seleccionada]/1000000, '.2f'))+"M"]
    la_tabla = pd.DataFrame({"Dato": indicadores, "Valor": datos_de_la_tabla})
    columns = [{"name": ["Resumen básico", "Dato"], "id": "Dato"}, 
               {"name": ["Resumen básico", "Valor"], "id": "Valor"}]
    data = [{"Dato": la_tabla["Dato"].values[i], 
             "Valor": la_tabla["Valor"].values[i]} for i in range(la_tabla.shape[0])]
    return data, columns


if __name__ == '__main__':
    app.run_server()
