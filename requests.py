import urllib.request
import json
import pandas as pd

def getElecByRegionAndYear(filtres):
    lignes = filtres["lignes"]
    annee = filtres["annee"]
    region = filtres["region"]
    filiere = filtres["filiere"]
    secteur = filtres["secteur"]
    
    lignesQuery = (f"&rows={urllib.parse.quote(lignes)}" if lignes else "&rows=10")
    anneeQuery = (f"&refine.annee={urllib.parse.quote(annee)}" if annee else "")
    regionQuery = (f"&refine.libelle_region={urllib.parse.quote(region)}" if region else "")
    filiereQuery = (f"&refine.filiere={urllib.parse.quote(filiere)}" if filiere else "")
    secteurQuery = (f"&refine.libelle_grand_secteur={urllib.parse.quote(secteur)}" if secteur else "")


    url = "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-naf-agregee-region&q=&facet=operateur&facet=annee&facet=filiere&facet=libelle_categorie_consommation&facet=libelle_grand_secteur&facet=libelle_secteur_naf2&facet=libelle_region"
    url += lignesQuery + anneeQuery + regionQuery + filiereQuery + secteurQuery

    response =  urllib.request.urlopen(url)
    data = json.loads(response.read())
    # data = pd.json_normalize(data).records

    dict = { "annee": [],
             "region": [],
             "conso": [],
             "secteur": [] }

    for entry in data["records"]:
        dict["annee"].append(entry["fields"]["annee"])
        dict["region"].append(entry["fields"]["libelle_region"])
        dict["conso"].append(entry["fields"]["conso"])
        dict["secteur"].append(entry["fields"]["libelle_grand_secteur"])


    dataframe = pd.DataFrame(dict)
    print(dataframe)
    return dataframe