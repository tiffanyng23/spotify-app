import requests 
import base64
import json
from api_requests import access_api

# get top tracks
artist_url ="https://api.spotify.com/v1/artists/6vWDO969PvNqNYHIOW5v0m/top-tracks"
artist_header = {
    "Authorization": f"Bearer {access_api.token}"
}

track_params = {
    "id": "6vWDO969PvNqNYHIOW5v0m",
    "market" : "CA"
}
try:
    response = requests.get(artist_url, headers = artist_header, params = track_params)

    response.raise_for_status()
    print(f"Top Tracks Request: {response.status_code}")
except requests.exceptions.HTTPError as http_error:
    print(f"Top Tracks Request HTTP Error: {http_error}")
except requests.exceptions.RequestException as error:
    print(f"Top Tracks Request Other Error: {error}")

artist_tracks = response.json()["tracks"]
for track in artist_tracks:
    album = track["album"]["name"]
    name = track["name"]
    rank = track["popularity"]
    preview = track["preview_url"]
    print(f"{album}:{name} ({rank})")

    