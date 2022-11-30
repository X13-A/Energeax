# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
import pandas as pd

app = Dash(__name__)

annees = [i for i in range(2011, 2022)]
annees.reverse()

app.layout = html.Div([
    html.Div(children=[
        
        html.Br(),
        html.Label('Sélectionnez une filiaire'),
        dcc.RadioItems(['Electricité', 'Gaz'], 'Electricité'),

        html.Br(),
        html.Label('Sélectionnez un ou plusieurs secteurs'),
        dcc.Dropdown(['Tertiaire',
                    'Industrie',
                    'Secteur Inconnu',
                    'Agriculture',
                    'Résidentiel'],
                     multi=True),

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
                     multi=True),
        
        html.Br(),
        html.Label('Sélectionnez une année'),
        dcc.Dropdown(annees, multi=False),

    ], style={'padding': 10, 'flex': 1}),
], style={'display': 'flex', 'flex-direction': 'row'})

@app.callback(
    Output(component_id='body-div', component_property='children'),
    Input(component_id='show-secret', component_property='n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Elephants are the only animal that can't jump"

if __name__ == '__main__':
    app.run_server(debug=True)