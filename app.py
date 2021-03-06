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
                    delimiter = "\t", nrows = 6250)
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

# Lista de diccionarios (con estructura "label" y "value" obligatoriamente)
# de periodos para definir el intervalo del gráfico:
periodos = [{"label": "1 año", "value": "1 año"}, 
            {"label": "6 meses", "value": "6 meses"}, 
            {"label": "3 meses", "value": "3 meses"}, 
            {"label": "1 mes", "value": "1 mes"}]            

# Diccionario con el número de meses atrás a considerar para cada periodo:
meses = {"1 año": 12, "6 meses": 6, "3 meses": 3, "1 mes": 1}

# Lista de indicadores técnicos:
lista_indicadores_superiores = ["Bollinger Bands", "EMA", "Parabolic SAR"]
lista_indicadores_inferiores = ["MACD", "RSI"]


# Diccionario de diccionarios con información de composición accionaria:
# En el caso de empresas con acciones preferenciales es la suma de preferenciales y ordinarias
composicion_accionaria = {"BCOLOMBIA": {"Grupo de Inversiones Suramericana": 234027881,
                                        "Fdo. Bancolombia ADR Program": 156917764, 
                                        "FPO Porvenir Moderado": 50883394+23502497, 
                                        "FPO Protección Moderado": 21048882+53667418, 
                                        "Otros":421779164}, 
                          "BOGOTA": {"Grupo Aval Acciones y Valores S.A": 227710487, 
                                     "Consultorías de Inversiones S.A": 32140397, 
                                     "Rendifin S.A": 11439891, 
                                     "Adminegocios & Cia SCA": 9062222, 
                                     "Otros":50927558},
                          "BVC": {"Utilico Emerging Markets Trust PLC": 4724436, 
                                  "BBVA Colombia S.A": 4436539, 
                                  "Banco Davivienda S.A": 3825700, 
                                  "B3 S.A": 3697218, 
                                  "Otros": 43829576}, 
                          "CELSIA": {"Grupo Argos S.A": 566360307, 
                                     "FPO Porvenir Moderado": 85229516, 
                                     "FPO Protección Moderado": 82110895, 
                                     "Fdo. Bursatil Ishares Colcap": 35527384, 
                                     "Otros": 300744452},
                          "CEMARGOS": {"Grupo Argos S.A": 668786536, 
                                       "FPO Protección Moderado": 67452055+35915250, 
                                       "FPO Porvenir Moderado": 49712014+45820462,
                                       "Fdo. Bursatil Ishares Colcap": 34521509+14545954, 
                                       "Otros": 444116380},
                          "CNEC": {"CDS & Co": 102089967, 
                                   "CEDE & Co": 46154417, 
                                   "Doverton Investments S.A": 6072154, 
                                   "Fdo. Bursatil Ishares Colcap": 5735630, 
                                   "Otros": 17570832},
                          "CONCONCRET": {"Vinci Colombie S.A.S": 226850988, 
                                         "Patrimonio Autónomo San Luis": 84728844, 
                                         "Idearlu S.A.S": 60002086, 
                                         "FPO Colfondos Moderado": 55011365, 
                                         "Otros": 707661656},
                          "CORFICOLCF": {"Banco de Bogotá S.A": 110401769, 
                                         "Adminegocios S.A.S": 35714947, 
                                         "Grupo Aval Acciones y Valores S.A": 27270567, 
                                         "Banco Popular S.A": 16522863, 
                                         "Otros": 134100862}, 
                          "ECOPETROL": {"Entidades Estatales": 36384788417, 
                                        "JP Morgan Chase Bank NA FBO Holders Of DR Ecopetrol": 800624420, 
                                        "FPO Porvenir Moderado": 420491354, 
                                        "FPO Protección Moderado": 334489075, 
                                        "Otros": 3176301424}, 
                          "ETB": {"Bogotá Distrito Capital": 3066154179, 
                                  "Persona natural": 100005238, 
                                  "Universidad Distrital Francisco José de Caldas": 71011068, 
                                  "Amber Global Opportunities Ltd": 68912646, 
                                  "Otros": 244470281}, 
                          "EXITO": {"Sendas Distribuidora S.A.S": 432256668, 
                                    "Fdo. Bursatil Ishares Colcap": 5662510, 
                                    "FPO Protección Mayor Riesgo": 1325159, 
                                    "Fdo. Pensiones Protección - PI": 1271681, 
                                    "Otros": 7088298}, 
                          "GEB": {"Bogotá Distrito Capital": 6030406241, 
                                  "FPO Porvenir Moderado": 773621230, 
                                  "FPO Protección Moderado": 547711351, 
                                  "Corporación Financiera Colombiana S.A": 475298648, 
                                  "Otros": 1354139547}, 
                          "GRUPOARGOS": {"Grupo de Inversiones Suramericana S.A": 229295179, 
                                         "Grupo Nutresa S.A": 79804628, 
                                         "FPO Protección Moderado": 22668983+44166780, 
                                         "FPO Porvenir Moderado": 25892288+35376989, 
                                         "Otros": 420022333}, 
                          "GRUPOAVAL": {"Adminegocios S.A.S":  6094903964+29645670, 
                                        "Actiunidos S.A": 3028922128+687451726, 
                                        "El Zuque S.A": 561052547+958153905, 
                                        "Inversiones Escorial S.A": 1270118990, 
                                        "Otros": 9650768229}, 
                          "GRUPOSURA": {"Grupo Argos S.A": 129721643, 
                                        "Grupo Nutresa S.A": 61021436, 
                                        "FPO Protección Moderado": 49608442, 
                                        "FPO Porvenir Moderado": 47499236, 
                                        "Otros": 294126791}, 
                          "ISA": {"MHCP": 569472561, 
                                  "EPM E.S.P": 97724413, 
                                  "FPO Porvenir Moderado": 92375588, 
                                  "FPO Protección Moderado": 63707822, 
                                  "Otros": 284397510}, 
                          "NUTRESA": {"Grupo de Inversiones Suramericana S.A": 161014311, 
                                      "Grupo Argos S.A": 46350817, 
                                      "FPO Porvenir Moderado": 29830733, 
                                      "Fdo. Bursatil Ishares Colcap": 17175713, 
                                      "Otros": 205751884}, 
                          "PFAVAL": {"Adminegocios S.A.S":  6094903964+29645670, 
                                     "Actiunidos S.A": 3028922128+687451726, 
                                     "El Zuque S.A": 561052547+958153905, 
                                     "Inversiones Escorial S.A": 1270118990, 
                                     "Otros": 9650768229}, 
                          "PFBCOLOM": {"Grupo de Inversiones Suramericana": 234027881,
                                       "Fdo. Bancolombia ADR Program": 156917764, 
                                       "FPO Porvenir Moderado": 50883394+23502497, 
                                       "FPO Protección Moderado": 21048882+53667418, 
                                       "Otros":421779164}, 
                          "PFCEMARGOS": {"Grupo Argos S.A": 668786536, 
                                         "FPO Protección Moderado": 67452055+35915250, 
                                         "FPO Porvenir Moderado": 49712014+45820462,
                                         "Fdo. Bursatil Ishares Colcap": 34521509+14545954, 
                                         "Otros": 444116380}, 
                          "PFDAVVNDA": {"Inveranagrama S.A.S": 72625101, 
                                        "Inversiones Financieras Bolivar S.A.S": 72563201, 
                                        "Inversiones Cusezar S.A": 41044772, 
                                        "Grupo Bolivar S.A": 40805701, 
                                        "Otros": 224631638}, 
                          "PFGRUPOARG": {"Grupo de Inversiones Suramericana S.A": 229295179, 
                                         "Grupo Nutresa S.A": 79804628, 
                                         "FPO Protección Moderado": 22668983+44166780, 
                                         "FPO Porvenir Moderado": 25892288+35376989, 
                                         "Otros": 420022333}, 
                          "PFGRUPSURA": {"Grupo Argos S.A": 129721643, 
                                         "Grupo Nutresa S.A": 61021436, 
                                         "FPO Protección Moderado": 49608442, 
                                         "FPO Porvenir Moderado": 47499236, 
                                         "Otros": 294126791}}
                                  

# Inicializar la aplicación:
# Los ORIGINALES SON:
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
    html.Div([
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
    html.Div([html.P("Seleccione un periodo:", className = "control_label"), 
              dcc.Dropdown(id = "dropdown_fechas", options = periodos, value = "6 meses"),
              dcc.Graph(id='grafico_principal')], className = "six columns"), 
    html.Div([html.H6("Información"), 
              dash_table.DataTable(id = "tabla_resumen", 
                                   data = [], 
                                   columns = [{"name": ["Resumen básico", "Dato"], "id": "Dato"}, 
                                              {"name": ["Resumen básico", "Valor"], "id": "Valor"}], 
                                   style_cell={'fontSize':13, 'fontFamily':'sans-serif', 'textAlign': 'left'}, 
                                   merge_duplicate_headers = True,
                                   style_as_list_view=True, 
                                   style_header = {'fontWeight': 'bold'}, 
                                   style_data = {'whiteSpace': 'normal', 'height': 'auto'},
                                   style_data_conditional=([{'if': {'filter_query': '{Valor} contains "-" && {Valor} contains "%"','column_id': 'Valor'},
                                                             'color': 'red'}]))], 
             className = "three columns")], 
             className = "row"),
    html.Br(),
    html.Div([dcc.Graph(id = 'grafico_accionistas')], className = "pretty_container five columns")
])



# Definir callbacks:

# Actualizar gráfico principal con la acción seleccionada:
@app.callback(Output('grafico_principal', 'figure'),
              [Input('dropdown', 'value'),
               Input('dropdown_fechas', 'value'), 
               Input('checklist_superiores', 'value'), 
               Input('checklist_inferiores', 'value')])
def grafica_principal(accion_seleccionada, intervalo_fechas, indicadores_superiores_seleccionados, indicadores_inferiores_seleccionados):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    fecha_mas_reciente = datos_seleccionados["Fecha"].max()
    periodo = meses[intervalo_fechas]
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
        grafico.add_bollinger_bands(periods = 10, name = "BOLL")
    else:
        a = 1
    
    if "EMA" in indicadores_superiores_seleccionados:
        grafico.add_ema(periods = 20, colors = "#ff55a3")
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
    el_grafico_principal.update_layout(showlegend = False)
    #el_graficio_principal.update_layout(yaxis_tickprefix = '$')
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
                    
    ultimo_precio = "$"+str(int(ultimo_precio))
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
              [Input("dropdown", "value"), 
               Input("dropdown_fechas", "value")])
def tabla_de_resumen(accion_seleccionada, intervalo_fechas):
    datos_seleccionados = datos[datos['Nemotecnico']==accion_seleccionada]
    periodo = meses[intervalo_fechas]
    # Selección de fechas:
    fecha_mas_reciente = datos_seleccionados["Fecha"].max()
    fecha_de_referencia_52_semanas = fecha_mas_reciente-DateOffset(months = 12)
    fecha_de_referencia_periodo_seleccionado = fecha_mas_reciente-DateOffset(months = periodo)
    ultimo_anio = datos_seleccionados["Fecha"].dt.year.max()
    fecha_YTD = datos_seleccionados[datos_seleccionados["Fecha"].dt.year >= ultimo_anio]["Fecha"].min() 
    # Selección de los datos para los correspondientes intervalos:
    datos_mas_recientes = datos_seleccionados[datos_seleccionados["Fecha"] == fecha_mas_reciente]
    datos_seleccionados_52_semanas = datos_seleccionados[datos_seleccionados["Fecha"]>= fecha_de_referencia_52_semanas]
    datos_seleccionados_periodo = datos_seleccionados[datos_seleccionados["Fecha"]>= fecha_de_referencia_periodo_seleccionado]
    # Precios de referencia:
    ultimo_precio = datos_mas_recientes["Cierre"].values[0]
    precio_inicial_YTD = datos_seleccionados[datos_seleccionados["Fecha"] == fecha_YTD]["Cierre"].values[0]
    maximo_52_semanas = datos_seleccionados_52_semanas["Cierre"].max()
    minimo_52_semanas = datos_seleccionados_52_semanas["Cierre"].min()
    maximo_periodo = datos_seleccionados_periodo["Cierre"].max()
    minimo_periodo = datos_seleccionados_periodo["Cierre"].min()
    # Rangos de precios:
    rango_52_semanas = "$" + str(int(minimo_52_semanas)) + "-" + "$" + str(int(maximo_52_semanas))
    rango_periodo = "$" + str(int(minimo_periodo))+ "-" + "$" + str(int(maximo_periodo))
    # Potenciales de valorización:
    potencial_al_maximo_52 = "+" + str(round(((maximo_52_semanas-ultimo_precio)/ultimo_precio)*100, 2))+"%"
    potencial_al_minimo_52 = str(round(((minimo_52_semanas-ultimo_precio)/ultimo_precio)*100, 2))+"%"
    YTD = str(round(((ultimo_precio - precio_inicial_YTD)/precio_inicial_YTD)*100, 2))+"%"
    indicadores = ["Rango 52 semanas:", "Rango periodo seleccionado:", 
                   "Potencial al Máx52:", "Potencial al Mín52:", "YTD",
                   "Emisor:", "En circulación:"]
    datos_de_la_tabla = [rango_52_semanas, rango_periodo, 
                         potencial_al_maximo_52, potencial_al_minimo_52, YTD, 
                         emisores[accion_seleccionada], 
                         str(format(numero_acciones[accion_seleccionada]/1000000, '.2f'))+"M"]
    la_tabla = pd.DataFrame({"Dato": indicadores, "Valor": datos_de_la_tabla})
    columns = [{"name": ["Resumen básico", "Dato"], "id": "Dato"}, 
               {"name": ["Resumen básico", "Valor"], "id": "Valor"}]
    data = [{"Dato": la_tabla["Dato"].values[i], 
             "Valor": la_tabla["Valor"].values[i]} for i in range(la_tabla.shape[0])]
    return data, columns

# Actualización de gráfico de accionistas:
@app.callback(Output("grafico_accionistas", "figure"), 
              [Input("dropdown", "value")])
def grafico_de_accionistas(accion_seleccionada):
    accionistas = list(composicion_accionaria[accion_seleccionada].keys())
    participaciones = list(composicion_accionaria[accion_seleccionada].values())
    fig = go.Figure(data=[go.Pie(labels=accionistas, values=participaciones, hole=.3)])
    fig.update_layout(legend={"xanchor": "center", 
                              "yanchor": "top",
                              "y": 0, 
                              "x": 0})
    return fig
if __name__ == '__main__':
    app.run_server()
