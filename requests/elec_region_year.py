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
    # Init dict
    dict = { "annee": [],
            "region": [],
            "conso": [],
            "secteur": [] }

    # Get data for each year
    for annee in filtres["annees"]:
        url = buildUrl(filtres["lignes"], annee, filtres["region"], filtres["filiere"], filtres["secteur"])
        response =  urllib.request.urlopen(url)
        data = json.loads(response.read())
        
        for entry in data["records"]:
            dict["annee"].append(annee)
            dict["region"].append(entry["fields"]["libelle_region"])
            dict["conso"].append(entry["fields"]["conso"])
            dict["secteur"].append(entry["fields"]["libelle_grand_secteur"])

    # Get total consumption for each year 
    consos = []
    dataframe = pd.DataFrame(dict)
    for annee in filtres["annees"]:
        consos.append(dataframe.loc[dataframe["annee"] == annee]["conso"].sum())
    
    # Return pandas frame
    return pd.DataFrame({
        "annee": filtres["annees"],
        "conso": consos
    })

# Test algorithm and print values:
filtres = {
    "annees" : [2021,2020,2019],
    "region" : "",
    "filiere" : "Electricité",
    "secteur" : "",
    "lignes" : "10000"
}

data = getElecByRegionAndYear(filtres)
print(data)