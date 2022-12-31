import urllib.request
import json
import pandas as pd
from requests.build_url import buildUrl
from constants import *

# Creates dict of dataframes for each region
def getElecByRegionAndYear(filtres):
    dataframes = {}

    # Create years list
    annees = [i for i in range(filtres["debut"], filtres["fin"]+1)]

    # Get data for each region
    for codeRegion in filtres["regions"]:
        # Init dict
        dict = { "annee": [],
                "conso": [], }

        # Get data for each year
        for annee in annees:
            url = buildUrl(filtres["lignes"], annee, codeRegion, filtres["filiere"], filtres["secteur"])
            response =  urllib.request.urlopen(url)
            data = json.loads(response.read())
            
            for entry in data["records"]:
                dict["annee"].append(annee)
                dict["conso"].append(entry["fields"]["conso"])

        # Calc total consumption for each year 
        consos = []
        dataframe = pd.DataFrame(dict)
        for annee in annees:
            consos.append(dataframe.loc[dataframe["annee"] == annee]["conso"].sum())
        
        # Return pandas frame
        
        nomRegion = [nom for code, nom in regions.items() if code == codeRegion][0]
        dataframes[nomRegion] = pd.DataFrame({
            "annee": annees,
            "conso": consos
        })
    return dataframes
