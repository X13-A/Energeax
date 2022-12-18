# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State
import json
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from requests.elec_region_year import getElecByRegionAndYear

#region variables
annees = [i for i in range(2011, 2022)]

regions = ['Grand Est',
            'Auvergne-Rhône-Alpes',
            'Occitanie',
            'Hauts-de-France',
            'Nouvelle-Aquitaine',
            'Centre-Val de Loire',
            'Bourgogne-Franche-Comté',
            'Provence-Alpes-Côte d\'Azur',
            'Île-de-France',
            'Normandie',
            'Pays de la Loire',
            'Bretagne',
            'La Réunion',
            'Guadeloupe',
            'Martinique',
            'Corse',
            'Guyane',
            'Non affecté à une région',
            'Mayotte']
            
secteurs = ['Tertiaire',
            'Industrie',
            'Secteur Inconnu',
            'Agriculture',
            'Résidentiel']

filtres = {
    "debut": "",
    "fin": "",
    "region" : "",
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
    html.Div([html.H1("EnergyBoard")], className="header"),
    html.Div([
        html.Div([
            html.Br(),
            html.Label('Sélectionnez une filière'),
            dcc.RadioItems(['Electricité', 'Gaz'], 'Electricité', id='filiere-radioitems'),
            html.Div(id='dd-output-filiere'),
        ]),
        html.Div([
            html.Br(),
            html.Label('Sélectionnez un ou plusieurs secteurs'),
            dcc.Dropdown(secteurs,
                        placeholder="Sélectionnez un ou plusieurs secteurs",
                        id='secteur-dropdown',
                        multi=False), 
            html.Div(id='dd-output-secteur'),
        ]),
        html.Div([
            html.Br(),
            html.Label('Sélectionnez une ou plusieurs régions'),
            dcc.Dropdown(regions,
                        placeholder="Sélectionnez une ou plusieurs régions",
                        id='region-dropdown',
                        multi=False),
            html.Div(id='dd-output-region'),
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
            html.Div(id='dd-output-update'),
        ]),
    ], className="menu"),
    html.Div([html.Div([html.H1("Hello world"), html.Br()], id='dd-output-data')], className="main"),
    dcc.Store(id='store'),
], className="content")

#endregion

#region Callback
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
    Output('dd-output-region', 'children'),
    Input('region-dropdown', 'value'),
)
def update_region(value):
    filtres["region"] = value


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
        data = getElecByRegionAndYear(filtres)
        titre = f"Consommation par année {'du secteur ' +  filtres['secteur'] if filtres['secteur'] else ''} en {filtres['region'] if filtres['region'] else 'France'}"
        fig = px.line(data, x='annee', y='conso', range_y=[0, data.max()*1.25], title=titre, labels={'annee': 'Année', 'conso': 'Consommation'})
        # fig.show()
        
        graph = dcc.Graph(figure = fig)

if __name__ == '__main__':
    app.run_server(debug=True)