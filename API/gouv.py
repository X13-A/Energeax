import urllib.request
import json
import pandas as pd

url = "https://opendata.agenceore.fr/api/records/1.0/search/?dataset=conso-elec-gaz-annuelle-par-naf-agregee-region&q=&rows=10&refine.annee=2021&refine.filiere=Electricit%C3%A9"
response =  urllib.request.urlopen(url)
data = json.loads(response.read())
test = pd.DataFrame.from_dict(data,orient ='index')

print(test.describe())