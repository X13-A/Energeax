
import pandas as pd

url = "https://api.deezer.com/editorial/0/charts"
editorial = pd.read_json(url)

# print(editorial)

playlists = []
for playlist in editorial.tracks.data:
    playlists.append(playlist.get("title"))

for playlist in playlists:
    print(playlist)