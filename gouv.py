import urllib.request
import json
import pandas as pd

def getElecByRegionAndYear(filiere, region = "", annee = "", lignes = "1000"):
    lignesQuery = (f"&rows={urllib.parse.quote(lignes)}" if lignes else "&rows=10")
    anneeQuery = (f"&refine.annee={urllib.parse.quote(annee)}" if annee else "")
    regionQuery = (f"&refine.libelle_region={urllib.parse.quote(region)}" if region else "")
    filiereQuery = (f"&refine.filiere={urllib.parse.quote(filiere)}" if filiere else "")

    url = f"https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-naf-agregee-region&q=&facet=operateur&facet=annee&facet=filiere&facet=libelle_categorie_consommation&facet=libelle_grand_secteur&facet=libelle_secteur_naf2&facet=libelle_region"
    url += lignesQuery + anneeQuery + regionQuery + filiereQuery

    response =  urllib.request.urlopen(url)
    data = json.loads(response.read())
    data = pd.DataFrame.from_dict(data, orient ='index')
    return data
    # print(data["records"])

    # dict = { "annee": [],
    #          "region": [],
    #          "conso": [] }

    # for entry in data.records:
    #     dict["annee"].append(entry.fields.annee)
    #     dict["region"].append(entry.fields.libelle_region)
    #     dict["conso"].append(entry.fields.conso)
    
    print(dict)

def main ():
    lignes = "1000"
    annee = "2021"
    region = "Île-de-France"
    filiere = "Electricité"
    getElecByRegionAndYear(filiere=filiere)

main()