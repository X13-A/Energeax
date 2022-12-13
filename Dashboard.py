# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from requests.elec_region_year import getElecByRegionAndYear

annees = [i for i in range(2011, 2022)]
annees.reverse()
data = None

filtres = {
    "annees" : [],
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
            dcc.Dropdown(annees, id='annee-dropdown', placeholder='Sélectionnez une année', multi=True),
            html.Div(id='dd-output-annee'),
        ]),
        html.Div([
            html.Br(),
            html.Button("Update", id="update-button", n_clicks=0),
            html.Div(id='dd-output-update'),
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

@app.callback(
    Output('dd-output-secteur', 'children'),
    Input('secteur-dropdown', 'value'),
)
def update_output(value):
    filtres["secteur"] = value

@app.callback(
    Output('dd-output-region', 'children'),
    Input('region-dropdown', 'value'),
)
def update_output(value):
    filtres["region"] = value

@app.callback(
    Output('dd-output-annee', 'children'),
    Input('annee-dropdown', 'value'),
)
def update_output(value):
    filtres["annees"] = value

@app.callback(
    Output('dd-output-update', 'children'),
    [Input('update-button', 'n_clicks')],
)
def update_output(value):
    update()


#endregion

def update():
    global data
    global filtres
    print (filtres)
    if (filtres["filiere"] and filtres["annees"] != None and len(filtres["annees"]) > 0):
        data = getElecByRegionAndYear(filtres)
        fig = px.line(data, x='annee', y='conso', range_y=[0, data.max()*1.25])
        fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)