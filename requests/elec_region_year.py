import urllib.request
import json
import pandas as pd
from requests.build_url import buildUrl

def getElecByRegionAndYear(filtres):
    dataframes = {}

    # Create years list
    annees = [i for i in range(filtres["debut"], filtres["fin"]+1)]

    for region in filtres["regions"]:
        # Init dict
        dict = { "annee": [],
                "conso": [], }

        # Get data for each year
        for annee in annees:
            url = buildUrl(filtres["lignes"], annee, region, filtres["filiere"], filtres["secteur"])
            response =  urllib.request.urlopen(url)
            data = json.loads(response.read())
            
            for entry in data["records"]:
                dict["annee"].append(annee)
                dict["conso"].append(entry["fields"]["conso"])

        # Get total consumption for each year 
        consos = []
        dataframe = pd.DataFrame(dict)
        for annee in annees:
            consos.append(dataframe.loc[dataframe["annee"] == annee]["conso"].sum())
        
        # Return pandas frame
        dataframes[region] = pd.DataFrame({
            "annee": annees,
            "conso": consos
        })
    return dataframes

def main():
    # Test algorithm and print values:
    filtres = {
        "debut" : 2017,
        "fin": 2021,
        "region" : "",
        "filiere" : "Electricité",
        "secteur" : "",
        "lignes" : "10000"
    }

    data = getElecByRegionAndYear(filtres)
    print(data)
