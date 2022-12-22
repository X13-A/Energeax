import urllib.request
import json
import pandas as pd
import folium
from build_url import buildUrl
from .. dashboard import regions

#style function
sf = lambda x :{'fillColor':'#8f95de', 'fillOpacity':0.5, 'color':'#6167ad', 'weight':1, 'opacity':1}

def getElecByYear(annee, filiere):
    dataframe = None
    consos = []
    # Get data for each region
    for region in regions:
        url = buildUrl("10000", annee, region, filiere, "")
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        sum = 0
        for entry in data["records"]:
            sum += entry["fields"]["conso"]
        consos.append(sum)
        
    # Return pandas frame
    dataframe = pd.DataFrame({
        "region": regions,
        "conso": consos
    })
    return dataframe

def createMap(annee, filiere):
    conso_data = getElecByYear(annee, filiere)
    coords = (48.7453229,2.5073644)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5)
    geo_data = None
    with open("regions_france.geojson", "r") as f:
        geo_data = json.load(f)

    folium.Choropleth(
        geo_data = geo_data,
        data=conso_data,
        name="france",
        columns=["region", "conso"],
        key_on="feature.properties.nom",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Consommation"
    ).add_to(map)
    map.save(outfile="france.html")

# Pour tester
# createMap("2021", "Electricité")
