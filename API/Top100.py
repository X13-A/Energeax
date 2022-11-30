import pandas as pd

url = "https://api.deezer.com/playlist/1109890291"
playlist = pd.read_json(url)

titles = []
for track in playlist.tracks.data:
    titles.append(track.get("title"))