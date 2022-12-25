# visit http://127.0.0.1:8050/ in your web browser.
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
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Consommation annuelle d'énergie par région", className="header-item"),
    ], className="header"),
    # App
    html.Div([
        # Menu
        html.Div([
            html.Div([
                html.Br(),
                html.Label('Affichage', className="input-label"),
                dcc.RadioItems(['Graphique', 'Carte'], 'Graphique', id='affichage-radioitems', className="radioItems"),
                html.Div(id='dd-output-affichage'),
            ]),
            html.Div([
                html.Br(),
                html.Label('Filière', className="input-label"),
                dcc.RadioItems(['Electricité', 'Gaz'], 'Electricité', id='filiere-radioitems', className="radioItems"),
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
            html.Div([
                html.Br(),
                html.Button("Update", id="update-button", className="modern-button", n_clicks=0),
                html.Button("Show", id="show-button", className="modern-button", n_clicks=0),
                html.Div(id='dd-output-update')
            ], className="button-group"),
            html.Div("Lorsque la mise à jour est terminée, cliquez sur \"show\" pour afficher les données.", className="info"),
        ], className="menu"),
        # Main
        html.Div([html.Div(id='dd-output-data')], className="main"),
        dcc.Store(id='store')
    ], className="app"),
    # Footer
    html.Div([
        html.Img(src="https://www.usinenouvelle.com/mediatheque/4/3/0/000271034_image_600x315.jpg",
        alt="logo de l'ESIEE Paris",
        className="picture"),
        html.Span("ESIEE Paris", className="header-item")
    ], className="footer"),
], className="content")
#endregion

#region Callbacks

#region update data and graph
@app.callback(
    Output('dd-output-data', 'children'), [Input('show-button', 'n_clicks')]
)
def update_graph(value):
    return html.Div([
        html.Div(graph)
        ])

@app.callback(
    Output('dd-output-update', 'children'),
    [Input('update-button', 'n_clicks')],
)
def update_data(value):
    update()
#endregion

#region filters
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

#endregion

def areInputsValid():
    filledInputs = filtres['debut'] and filtres['fin'] and filtres["filiere"]
    if not filledInputs: return False

    validDates = filtres['fin'] >= filtres['debut']
    if not validDates: return False
    
    return True

def update():
    global data
    global filtres
    global graph
    if areInputsValid():
        if not filtres["regions"]: filtres["regions"] = regions
        if filtres["affichage"] == "Graphique":
            titre = f"Consommation en Mégawatts par année {'du secteur ' +  filtres['secteur'] + ' ' if filtres['secteur'] else ''}en France"
            fig = go.Figure(layout_title_text=titre)
            fig.update_yaxes(title = "Consommation (MW)")
            fig.update_xaxes(title = "Année")
            dataframes = getElecByRegionAndYear(filtres)
            for frame in dataframes:
                fig = fig.add_trace(go.Scatter(x = dataframes[frame]["annee"], y = dataframes[frame]["conso"], name = frame))
            graph = dcc.Graph(figure = fig)
        elif filtres["affichage"] == "Carte":
            dataframe = getElecByYear(filtres)
            map = createMap(dataframe, filtres["regions"])
            map.save(outfile="france.html")
            graph = html.Iframe(id='map', className="map", srcDoc = open('france.html', 'r').read())



if __name__ == '__main__':
    app.run_server(debug=False)