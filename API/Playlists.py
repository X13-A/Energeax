import pandas as pd

url = "https://api.deezer.com/editorial/0/charts"
editorial = pd.read_json(url)

playlists = []
for playlist in editorial.playlists.data:
    playlists.append(playlist.get("title"))

for playlist in playlists:
    print(playlist)