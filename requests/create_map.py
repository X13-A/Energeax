import urllib.request
import json
import pandas as pd
import folium
from requests.build_url import buildUrl
from constants import *

# Gets data for map creation
def getElecByYear(filtres):
    # Init variables
    dataframe = None
    consos = []
    for region in filtres["regions"]:
        consos.append(0)
    annees = [i for i in range(filtres["debut"], filtres["fin"]+1)]

    # Get data for each year and region
    for annee in annees:
        i = 0
        for codeRegion in filtres["regions"]:
            url = buildUrl("10000", annee, codeRegion, filtres["filiere"], filtres["secteur"])
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            for entry in data["records"]:
                consos[i] += entry["fields"]["conso"]
            i += 1

    # Divide to get the average consumption instead of sum
    for i in range(len(consos)):
        consos[i] = consos[i] / len(annees)

    # Return dataframe
    dataframe = pd.DataFrame({
        "region": filtres["regions"],
        "conso": consos
    })
    return dataframe

# Creates map using dataframe
def createMap(dataframe, codesRegion):
    # Init map and load geodata
    coords = (48.7453229, 2.5073644)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5)
    geo_data = None
    with open("regions_france.geojson", "r") as f:
        geo_data = json.load(f)
    
    # Remove geodata for unwanted regions
    j = 0
    toRemove = [i for i, region in enumerate(geo_data["features"]) if region["properties"]["code"] not in codesRegion]
    for i in toRemove:
        geo_data["features"].pop(i - j)
        j += 1

    # Create map
    folium.Choropleth(
        geo_data=geo_data,
        data=dataframe,
        name="france",
        columns=["region", "conso"],
        key_on="feature.properties.code",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Consommation annuelle (MWh)"
    ).add_to(map)
    return map