# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd

annees = [i for i in range(2011, 2022)]
annees.reverse()
app = Dash(__name__)
app.layout = html.Div([
    
    html.Div([
        html.Div([
            html.Br(id='filiaire'),
            html.Label('Sélectionnez une filiaire'),
            dcc.RadioItems(['Electricité', 'Gaz'], 'Electricité'),
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
                        multi=True), 
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
                        multi=True),
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
        html.Div([ 'Inserer graph' ]),
    ])
], style={'padding': 10, 'display': 'flex'})

@app.callback(
    Output('dd-output-secteur', 'children'),
    Input('secteur-dropdown', 'value'),
)
def update_output(value):
    return f'Vous avez sélectionnez : {value}'

@app.callback(
    Output('dd-output-region', 'children'),
    Input('region-dropdown', 'value'),
)
def update_output(value):
    return f'Vous avez sélectionnez : {value}'

@app.callback(
    Output('dd-output-annee', 'children'),
    Input('annee-dropdown', 'value'),
)
def update_output(value):
    return f'Vous avez sélectionnez : {value}'

if __name__ == '__main__':
    app.run_server(debug=True)