# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, dcc, html, Input, Output, State
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

#region Dashboard
app = Dash(__name__)
app.title = 'Energeax'
app.layout = html.Div([
    # Header
    html.Div([
        html.Span("Energeax", className="header-item"),
        html.Span("La consommation en France", className="header-item"),
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
                                placeholder="Sélectionnez un secteur",
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
                html.Div("Lorsque la mise à jour est terminée, cliquez sur \"show\" pour afficher les données.", className="info"),
            ], className="menu"),
        ], className="left"),
        html.Div([
            # Navigation
            html.Div([        
                html.Div([html.Button('Didacticiel', id='tuto-button', className="tuto-button")], className="tuto"),
                html.Div([html.Button('Les données', id='data-button', className="data-button")], className="data"),
                html.Div([html.Button('Choix technologiques', id='technos-button', className="technos-button")], className="technos"),
            ], className="navigation"),

            # Main
            html.Div([html.Div(id='dd-output-data')], className="main"),
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

#region callbacks affichage
@app.callback(Output('dd-output-data', 'children'),
              [Input('tuto-button', 'n_clicks'),
               Input('data-button', 'n_clicks'),
               Input('technos-button', 'n_clicks'),
               Input('show-button', 'n_clicks')],
              [State('dd-output-data', 'children')])

def update_output(n_clicks1, n_clicks2, n_clicks3, n_clicks4, children):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'tuto-button':
            return html.Div(
                "Choisissez l'affichage que vous voulez, puis la filière qui vous intéresse, ainsi que les paramètres de votre recherche (secteur, régions et dates).\nEnsuite appuyer sur update, attendre la fin du chargement, appuyer sur affichage.",
                className="text"
            )
        elif button_id == 'data-button':
            return html.Div(
                "Nos données proviennent du site data.gouv, plus précisément de l'agence ORE.\nElles sont accessible avec lien suivant : https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-naf-agregee-region/api/",
                className="text"
            )
        elif button_id == 'technos-button':
            return html.Div(
                "Nous avons utilisés la biblitohèque python 'pandas' pour manipuler la donnée ainsi que 'plotly' pour générer le site WEB et les différents graphiques.",
                className="text"
            )
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

# Vérifie les inputs
def areInputsValid():
    validDates = True
    if filtres['fin'] and filtres['debut']:
        validDates = filtres['fin'] >= filtres['debut']
    
    if not validDates: return False
    
    return True

def update():
    global data
    global filtres
    global graph
    if areInputsValid():
        if not filtres["regions"]: filtres["regions"] = [code for code, nom in regions.items()]
        if not filtres ["debut"]: filtres["debut"] = 2021
        if not filtres ["fin"]: filtres["fin"] = 2021
        if not filtres ["debut"] and filtres["fin"]: filtres["debut"] == filtres["fin"]
        if not filtres ["fin"] and filtres["debut"]: filtres["fin"] == filtres["debut"]

        if filtres["affichage"] == "Graphique":
            titre = f"Consommation en Mégawatts par année {'du secteur ' +  filtres['secteur'] + ' ' if filtres['secteur'] else ''}en France"
            fig = go.Figure()
            fig.update_yaxes(title = "Consommation annuelle (MWh)")
            fig.update_xaxes(title = "Année")
            dataframes = getElecByRegionAndYear(filtres)
            for frame in dataframes:
                fig = fig.add_trace(go.Scatter(x = dataframes[frame]["annee"], y = dataframes[frame]["conso"], name = frame))
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                dcc.Graph(figure = fig)
            ])

        elif filtres["affichage"] == "Carte":
            dataframe = getElecByYear(filtres)
            map = createMap(dataframe, filtres["regions"])
            map.save(outfile="france.html")
            titre = ""
            if filtres['filiere'] == 'Electricité':
                titre = "Carte de la consommation d'electricité des régions françaises"
            elif filtres['filiere'] == 'Gaz':
                titre = "Carte de la consommation de gaz des régions françaises"
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                html.Iframe(id='map', className="map", srcDoc = open('france.html', 'r').read())
            ])

        elif filtres["affichage"] == "Histogramme":
            filtres['annee'] = filtres['fin']
            data = buildHistogram(filtres)
            dataframe = data["data"]
            min = 0
            max = math.sqrt(data["max"])

            fig = go.Figure()
            fig.update_yaxes(title = "Bâtiments dans la tranche de consommation")
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
                hover_text.append(f"{count} bâtiments ayant une consommation annuelle entre {consoMin} et {consoMax} MWh")

            # Set accurate Y labels
            n = 10
            tickvals = [round(min + ((max-min)/n)*i) for i in range(n+1)]
            fig.update_yaxes(tickvals=tickvals)
            ticktext=[str(round(n*n)) for n in tickvals]
            fig.update_yaxes(ticktext=ticktext)

            fig = fig.add_trace(go.Bar(x = shownFrame["conso"], y = shownFrame["count"], name = "Bar chart", text=hover_text))
            # fig = fig.add_trace(go.Scatter(x = shownFrame["conso"], y = shownFrame["count"], marker_color='black', name = "Curve", text=hover_text))
            
            titre = "Nombre de bâtiments dans chaque tranche de consommation"
            graph = html.Div([
                html.H2(titre, className="graph-title"),
                dcc.Graph(figure = fig)
            ])



if __name__ == '__main__':
    app.run_server(debug=True)