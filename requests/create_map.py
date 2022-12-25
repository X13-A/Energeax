import urllib.request
import json
import pandas as pd
import folium
from requests.build_url import buildUrl
from constants import *

#style function
sf = lambda x :{'fillColor':'#8f95de', 'fillOpacity':0.5, 'color':'#6167ad', 'weight':1, 'opacity':1}

def getElecByYear(filtres):
    dataframe = None

    consos = []
    for region in filtres["regions"]:
        consos.append(0)
    annees = [i for i in range(filtres["debut"], filtres["fin"]+1)]

    for annee in annees:
        i = 0
        for codeRegion in filtres["regions"]:
            url = buildUrl("10000", annee, codeRegion, filtres["filiere"], "")
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            for entry in data["records"]:
                consos[i] += entry["fields"]["conso"]
            i += 1

    # Moyenne sur toutes les années
    for i in range(len(consos)):
        consos[i] = consos[i] / len(annees)

    # Return pandas frame
    dataframe = pd.DataFrame({
        "region": filtres["regions"],
        "conso": consos
    })
    return dataframe

def createMap(dataframe, codesRegion):
    coords = (48.7453229, 2.5073644)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5)
    geo_data = None
    with open("regions_france.geojson", "r") as f:
        geo_data = json.load(f)
    
    j = 0
    toRemove = [i for i, region in enumerate(geo_data["features"]) if region["properties"]["code"] not in codesRegion]
    for i in toRemove:
        geo_data["features"].pop(i - j)
        j += 1

    folium.Choropleth(
        geo_data=geo_data,
        data=dataframe,
        name="france",
        columns=["region", "conso"],
        key_on="feature.properties.code",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Consommation"
    ).add_to(map)
    return map

# Pour tester
# filtres = {
#     "affichage": "Carte",
#     "debut": 2020,
#     "fin": 2021,
#     "regions" : ['Grand Est',
#                 'Auvergne-Rhône-Alpes',
#                 'Occitanie',
#                 'Hauts-de-France',
#                 'Nouvelle-Aquitaine',
#                 'Centre-Val de Loire',
#                 'Bourgogne-Franche-Comté',
#                 'Provence-Alpes-Côte d\'Azur',
#                 'Île-de-France',
#                 'Normandie',
#                 'Pays de la Loire',
#                 'Bretagne',
#                 'La Réunion',
#                 'Guadeloupe',
#                 'Martinique',
#                 'Corse',
#                 'Guyane',
#                 'Non affecté à une région',
#                 'Mayotte'],
#     "filiere" : "Electricité",
#     "secteur" : "",
#     "lignes" : "10000"
# }

# dataframe = getElecByYear(filtres)
# createMap(dataframe)
