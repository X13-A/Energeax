import urllib.request
import json
import pandas as pd

def buildUrl(lignes, annee, region, filiere, secteur):
    # Parse query params according to API
    lignesQuery = (f"&rows={urllib.parse.quote(lignes)}" if lignes else "&rows=10000")
    anneeQuery = (f"&refine.annee={urllib.parse.quote(str(annee))}" if annee else "")
    regionQuery = (f"&refine.libelle_region={urllib.parse.quote(region)}" if region else "")
    filiereQuery = (f"&refine.filiere={urllib.parse.quote(filiere)}" if filiere else "")
    secteurQuery = (f"&refine.libelle_grand_secteur={urllib.parse.quote(secteur)}" if secteur else "")
    # Build url
    url = "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-naf-agregee-region&q=&facet=operateur&facet=annee&facet=filiere&facet=libelle_categorie_consommation&facet=libelle_grand_secteur&facet=libelle_secteur_naf2&facet=libelle_region"
    url += lignesQuery + anneeQuery + regionQuery + filiereQuery + secteurQuery
    return url

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
