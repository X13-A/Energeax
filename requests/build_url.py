import urllib

def buildUrl(lignes, annee, region, filiere, secteur):
    # Parse query params according to API
    lignesQuery = (f"&rows={urllib.parse.quote(lignes)}" if lignes else "&rows=10000")
    anneeQuery = (f"&refine.annee={urllib.parse.quote(str(annee))}" if annee else "")
    regionQuery = (f"&refine.code_region={urllib.parse.quote(region)}" if region else "")
    filiereQuery = (f"&refine.filiere={urllib.parse.quote(filiere)}" if filiere else "")
    secteurQuery = (f"&refine.libelle_grand_secteur={urllib.parse.quote(secteur)}" if secteur else "")
    # Build url
    url = "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-naf-agregee-region&q=&facet=operateur&facet=annee&facet=filiere&facet=libelle_categorie_consommation&facet=libelle_grand_secteur&facet=libelle_secteur_naf2&facet=libelle_region"
    url += lignesQuery + anneeQuery + regionQuery + filiereQuery + secteurQuery
    return url