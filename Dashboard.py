# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from requests import getElecByRegionAndYear

annees = [i for i in range(2011, 2022)]
annees.reverse()
data = None

filtres = {
    "annee" : "",
    "region" : "",
    "filiere" : "",
    "secteur" : "",
    "lignes" : "10000"
}

#region Dashboard

app = Dash(__name__)
app.layout = html.Div([
    
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
            dcc.Dropdown(['Tertiaire',
                        'Industrie',
                        'Secteur Inconnu',
                        'Agriculture',
                        'Résidentiel'],
                        placeholder="Sélectionnez un ou plusieurs secteurs",
                        id='secteur-dropdown',
                        multi=False), 
            html.Div(id='dd-output-secteur'),
        ]),
        html.Div([
            html.Br(),
            html.Label('Sélectionnez une ou plusieurs régions'),
            dcc.Dropdown(['Grand Est',
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
                        'Mayotte'],
                        placeholder="Sélectionnez une ou plusieurs régions",
                        id='region-dropdown',
                        multi=False),
            html.Div(id='dd-output-region'),
        ]),
        html.Div([
            html.Br(),
            html.Label('Sélectionnez une année'),
            dcc.Dropdown(annees, id='annee-dropdown', multi=False, placeholder='Sélectionnez une année'),
            html.Div(id='dd-output-annee'),
        ]),
    ], style={'padding': 10, 'display': 'flex', 'flex-direction': 'column'}),

    html.Div([
        html.Div([ str(data) ]),
    ])
], style={'padding': 10, 'display': 'flex'})

#endregion

#region Callback

@app.callback(
    Output('dd-output-filiere', 'children'),
    Input('filiere-radioitems', 'value'),
)
def update_output(value):
    filtres["filiere"] = value
    update()

@app.callback(
    Output('dd-output-secteur', 'children'),
    Input('secteur-dropdown', 'value'),
)
def update_output(value):
    filtres["secteur"] = value
    update()

@app.callback(
    Output('dd-output-region', 'children'),
    Input('region-dropdown', 'value'),
)
def update_output(value):
    filtres["region"] = value
    update()

@app.callback(
    Output('dd-output-annee', 'children'),
    Input('annee-dropdown', 'value'),
)
def update_output(value):
    if value:
        filtres["annee"] = str(value)
        update()

#endregion

def update():
    if (filtres["filiere"] and filtres["annee"]):
        data = getElecByRegionAndYear(filtres)
    

if __name__ == '__main__':
    app.run_server(debug=True)