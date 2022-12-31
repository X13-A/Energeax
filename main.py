# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context
import json
import folium
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from requests.elec_region_year import getElecByRegionAndYear
from requests.create_map import createMap
from requests.create_map import getElecByYear
from requests.histogram import buildHistogram
import math
from constants import *

#region variables
filtres = {
    "affichage": "",
    "debut": "",
    "fin": "",
    "regions" : [],
    "filiere" : "",
    "secteur" : "",
    "lignes" : "10000"
}

data = pd.DataFrame([])
graph = None
#endregion

#region welcome page
def getWelcomePage():
    list1 = [
        "Choisissez le type d'affichage que vous voulez",
        "Configurez vos filtres",
        "Cliquez sur update",
        "Quand le traitement des données est terminé, cliquez sur \"Afficher\""
    ]
    list2 = [
        "Pour les secteurs: Tout est selectionné",
        "Pour les régions: Tout est selectionné",
        "Pour la période: L'année 2021 est selectionnée"
    ]
    list3 = [
        "Si une seule valeur est choisie, elle seule sera retenue",
        "Si deux valeurs sont choisies, un intervalle entre le début et la fin sera utilisé",
        "Les données ne s'actualiseront pas si l'intervalle est invalide (début > fin)",
        "Pour l'histogramme, seul la date de fin est retenue"
    ]
    list4 = [
        "Le graphique permet d'étudier l'évolution de la consommation de plusieurs régions de façon superposée",
        "La carte affiche la moyenne de consommation de chaque région pour la période choisie",
        "L'histogramme compte le nombre de lieux dans chaque tranche de consommation"
    ]
    return html.Div([
        html.H5("Pour afficher les données:", className="list-title"),
        html.Ul([html.Li(item, className="list-item") for item in list1], className="list"),
        html.H5("Si rien n'est spécifié dans le filtre:", className="list-title"),
        html.Ul([html.Li(item, className="list-item") for item in list2], className="list"),
        html.H5("Fonctionnement du filtre début / fin:", className="list-title"),
        html.Ul([html.Li(item, className="list-item") for item in list3], className="list"),
        html.H5("Les 3 types d'affichages:", className="list-title"),
        html.Ul([html.Li(item, className="list-item") for item in list4], className="list"),
        ],
        className="text"
    )
#endregion

#region Dashboard
app = Dash(__name__)
app.title = 'Energeax'
app.layout = html.Div([
    # Header
    html.Div([
        html.Span("La France et l'énergie", className="header-item"),
        html.Div(
            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_France.svg",
            alt="Drapeau français",
            className="logo")
        ),
    ], className="header"),
    # App
    html.Div([
        html.Div([
            # Menu
            html.Div([
                html.Div([
                    html.Br(),
                    html.Label('Affichage', className="input-label"),
                    dcc.RadioItems(['Graphique', 'Carte', 'Histogramme'], 'Graphique', id='affichage-radioitems',className="radioItems", inputStyle={"margin-right": "0.3rem"}),
                    html.Div(id='dd-output-affichage'),
                ]),
                html.Div([
                    html.Br(),
                    html.Label('Filière', className="input-label"),
                    dcc.RadioItems(['Electricité', 'Gaz'], 'Electricité', id='filiere-radioitems', className="radioItems", inputStyle={"margin-right": "0.3rem"}),
                    html.Div(id='dd-output-filiere'),
                ]),
                html.Div([
                    html.Br(),
                    html.Label('Secteur'),
                    dcc.Dropdown(secteurs,
                                placeholder="Tous les secteurs",
                                id='secteur-dropdown',
                                multi=False), 
                    html.Div(id='dd-output-secteur'),
                ]),
                html.Div([
                    html.Br(),
                    html.Label('Sélectionnez une ou plusieurs régions'),
                    dcc.Dropdown(regions,
                                placeholder="Toutes les régions",
                                id='regions-dropdown',
                                multi=True),
                    html.Div(id='dd-output-regions'),
                ]),
                html.Div([
                    html.Br(),
                    html.Label('Date de début'),
                    dcc.Dropdown(annees, id='debut-dropdown', placeholder='Sélectionnez une année', multi=False),
                    html.Div(id='dd-output-debut'),
                ]),
                html.Div([
                    html.Br(),
                    html.Label('Date de fin'),
                    dcc.Dropdown(annees, id='fin-dropdown', placeholder='Sélectionnez une année', multi=False),
                    html.Div(id='dd-output-fin'),
                ]),
                html.Div("L'année 2021 est selectionnée par défaut", className="info"),
                html.Div([
                    html.Br(),
                    html.Button("Update", id="update-button", className="modern-button", n_clicks=0),
                    html.Button("Afficher", id="show-button", className="modern-button", n_clicks=0),
                    html.Div(id='dd-output-update')
                ], className="button-group"),
                html.Div("Lorsque la mise à jour est terminée, cliquez sur \"Afficher\" pour afficher les données.", className="info"),
            ], className="menu"),
        ], className="left"),
        html.Div([
            # Navigation
            html.Div([        
                html.Div([html.Button('Prise en main', id='tuto-button', className="tuto-button")], className="tuto"),
                html.Div([html.Button('Les données', id='data-button', className="data-button")], className="data"),
                html.Div([html.Button('Technologies', id='technos-button', className="technos-button")], className="technos"),
            ], className="navigation"),

            # Main
            html.Div([html.Div(getWelcomePage(), id='dd-output-data')], className="main"),
            dcc.Store(id='store')
        ], className="right")
    ], className="app"),
    # Footer
    html.Div([
        html.Div("Alex Foulon & Erwan Gautier", className="Auteurs"),
        html.Div(
            html.Img(src="https://www.usinenouvelle.com/mediatheque/4/3/0/000271034_image_600x315.jpg",
            alt="logo de l'ESIEE Paris",
            className="logo")
        ),
    ], className="footer"),
], className="content")
#endregion

#region display callbacks
@app.callback(Output('dd-output-data', 'children'),
              [Input('tuto-button', 'n_clicks'),
               Input('data-button', 'n_clicks'),
               Input('technos-button', 'n_clicks'),
               Input('show-button', 'n_clicks')],
              [State('dd-output-data', 'children')])

# Updates display in main
def update_output(n_clicks1, n_clicks2, n_clicks3, n_clicks4, children):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'tuto-button':
            return getWelcomePage()
        elif button_id == 'data-button':
            return html.Div(
                [
                    html.H5("Provenance des données:", className="list-title"),
                    html.Div("Nos données proviennent du site data.gouv, plus précisément de l'agence ORE."),
                    html.Div([
                        html.Span("Elles sont accessible avec lien suivant : "),
                        html.A("https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-naf-agregee-region/api/", href="https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-naf-agregee-region/api/")
                    ])
                ],
                className="text"
            )
        elif button_id == 'technos-button':
            list = [
                "\"Dash\" pour le dashboard",
                "\"Plotly\" pour les graphiques",
                "\"Folium\" pour la carte",
                "\"Pandas\" pour le traitement des données"
            ]
            return html.Div([
                html.H5("Pour réaliser ce dashboard, les modules suivants ont été utilisés:", className="list-title"),
                html.Ul([html.Li(item, className="list-item") for item in list], className="list"),
            ], className="text")

        # Affiche le graphique
        elif button_id == 'show-button':
            return html.Div([
                html.Div(graph)
            ])
    return children
#endregion

#region callbacks data
@app.callback(
    Output('dd-output-update', 'children'),
    [Input('update-button', 'n_clicks')],
)
def update_data(value):
    if value > 0:
        update()
#endregion

#region callbacks filters
@app.callback(
    Output('dd-output-affichage', 'children'),
    Input('affichage-radioitems', 'value'),
)
def update_affichage(value):
    filtres["affichage"] = value

@app.callback(
    Output('dd-output-filiere', 'children'),
    Input('filiere-radioitems', 'value'),
)
def update_filiere(value):
    filtres["filiere"] = value

@app.callback(
    Output('dd-output-secteur', 'children'),
    Input('secteur-dropdown', 'value'),
)
def update_secteur(value):
    filtres["secteur"] = value

@app.callback(
    Output('dd-output-regions', 'children'),
    Input('regions-dropdown', 'value'),
)
def update_region(value):
    filtres["regions"] = value

@app.callback(
    Output('dd-output-debut', 'children'),
    Input('debut-dropdown', 'value'),
)
def update_debut(value):
    filtres["debut"] = value

@app.callback(
    Output('dd-output-fin', 'children'),
    Input('fin-dropdown', 'value'),
)
def update_fin(value):
    filtres["fin"] = value
#endregion

# Checks inputs
def areInputsValid():
    validDates = True
    if filtres['fin'] and filtres['debut']:
        validDates = filtres['fin'] >= filtres['debut']
    
    if not validDates: return False
    

    return True

# Updates the data according to the filters
def update():
    global data
    global filtres
    global graph
    if areInputsValid():
        # Sets all regions by default
        if not filtres["regions"]: filtres["regions"] = [code for code, nom in regions.items()]

        # Sets proper dates for the algorithms
        if not filtres ["debut"] and filtres["fin"]: filtres["debut"] = filtres["fin"]
        if not filtres ["fin"] and filtres["debut"]: filtres["fin"] = filtres["debut"]
        if not filtres ["debut"]: filtres["debut"] = 2021
        if not filtres ["fin"]: filtres["fin"] = 2021

        # Creates a graph
        if filtres["affichage"] == "Graphique":
            titre = f"Consommation en Mégawatts par année {'du secteur ' +  filtres['secteur'] + ' ' if filtres['secteur'] else ''}en France"
            fig = go.Figure()
            fig.update_yaxes(title = "Consommation annuelle (MWh)")
            fig.update_xaxes(title = "Année")
            dataframes = getElecByRegionAndYear(filtres)
            
            # Adds all traces to the figure
            for frame in dataframes:
                fig = fig.add_trace(go.Scatter(x = dataframes[frame]["annee"], y = dataframes[frame]["conso"], name = frame))
            
            # Sets graph for use
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                dcc.Graph(figure = fig)
            ])

        # Creates a map
        elif filtres["affichage"] == "Carte":
            dataframe = getElecByYear(filtres)
            map = createMap(dataframe, filtres["regions"])
            map.save(outfile="france.html")

            # Generate title
            titre = ""
            if filtres['filiere'] == 'Electricité':
                titre = "Carte de la consommation d'electricité des régions françaises"
            elif filtres['filiere'] == 'Gaz':
                titre = "Carte de la consommation de gaz des régions françaises"
            if filtres['fin'] != filtres['debut']:
                titre += f" entre {filtres['debut']} et {filtres['fin']}"
            else:
                titre += f" en {filtres['fin']}" 
            if filtres['secteur']: titre += f" (secteur: {filtres['secteur']})"
            
            # Set map for use
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                html.Iframe(id='map', className="map", srcDoc = open('france.html', 'r').read())
            ])

        # Creates an histogram
        elif filtres["affichage"] == "Histogramme":
            filtres['annee'] = filtres['fin']
            data = buildHistogram(filtres)
            dataframe = data["data"]

            # Setup figure
            min = 0
            max = math.sqrt(data["max"])

            fig = go.Figure()
            fig.update_yaxes(title = f"lieux dans la tranche de consommation")
            fig.update_yaxes(range=[min, max])
            fig.update_xaxes(title = "Consommation annuelle (MWh)")

            # Flatten Y axis for readability
            shownFrame = {
                "count": [],
                "conso": [x for x in dataframe["conso"]]
            }

            for count in dataframe["count"]:
                shownFrame["count"].append(math.sqrt(count))

            shownFrame = pd.DataFrame(shownFrame)

            # Set accurate ToolTip
            hover_text = []
            for i in range(len(dataframe)):
                count = dataframe.loc[i, "count"]
                consoMax = dataframe.loc[i, "conso"]
                consoMin = 0
                if i > 0: consoMin = dataframe.loc[i-1, "conso"]
                hover_text.append(f"{count} lieux ayant une consommation annuelle entre {consoMin} et {consoMax} MWh")

            # Set accurate Y labels
            n = 10
            tickvals = [round(min + ((max-min)/n)*i) for i in range(n+1)]
            fig.update_yaxes(tickvals=tickvals)
            ticktext=[str(round(n*n)) for n in tickvals]
            fig.update_yaxes(ticktext=ticktext)

            
            # Generate title
            titre = f"Nombre de lieux dans chaque tranche de consommation en {filtres['fin']}"
            if filtres['secteur']: titre += f" (secteur: {filtres['secteur']})"

            # Set histogram for use
            fig = fig.add_trace(go.Bar(x = shownFrame["conso"], y = shownFrame["count"], name = "Bar chart", text=hover_text))
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                html.Div([
                    html.H5("Pour des raisons de lisibilité, l'axe Y grandit de façon non linéare", style={"text-align": "center"})
                ], className="text"),
                dcc.Graph(figure = fig),
            ])

if __name__ == '__main__':
    app.run_server(debug=True)
