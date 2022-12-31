import urllib.request
import json
import pandas as pd
from requests.build_url import buildUrl
import math

def buildHistogram(filtres):
    min = math.inf
    max = 0

    intervals = []
    counts = {}
    datasets = {}

    # fetch data
    for code_region in filtres["regions"]:
        url = buildUrl("10000", filtres["annee"], code_region, filtres["filiere"], "")
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        datasets[code_region] = data

    # set min and max values
    for data in datasets.values():
        for entry in data["records"]:
            conso = entry["fields"]["conso"]
            if conso < min: min = conso
            if conso > max: max = conso

    # set consumption ranges
    n = 100
    intervals = [min + ((max-min)/n)*i for i in range(n+1)]
    counts = {}
    for interval in intervals:
        counts[interval] = 0

    # count occurences for each range
    for data in datasets.values():
        for entry in data["records"]:
            for interval in intervals:
                if entry["fields"]["conso"] <= interval:
                    counts[interval] += 1
                    break
    
    # remove empty intervals
    for interval in intervals:
        if counts[interval] == 0: counts.pop(interval, None)

    # format dict for panda
    dataframe = {
        "conso": [],
        "count": []
    }

    minCount = math.inf
    maxCount = 0
    for conso, count in counts.items():
        dataframe["conso"].append(str(conso))
        dataframe["count"].append(count)
        if count < minCount: minCount = count
        if count > maxCount: maxCount = count


    return {
        "min": minCount,
        "max": maxCount,
        "data": pd.DataFrame(dataframe)
    } 


# filtres = {
#     "affichage": "Carte",
#     "annee": 2021,
#     "regions" : ['11', '94'],
#     "filiere" : "Electricité",
#     "secteur" : "",
#     "lignes" : "10000"
# }

# dataframe = buildHistogram(filtres)

# print(dataframe)