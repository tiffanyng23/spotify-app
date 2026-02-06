import requests 
import base64
import json
from api_requests import access_api


#request artist albums data
artist_url ="https://api.spotify.com/v1/artists/6vWDO969PvNqNYHIOW5v0m/albums"
artist_header = {
    "Authorization": f"Bearer {access_api.token}"
}
# query string used for requests.get
album_params = {
    "id": "6vWDO969PvNqNYHIOW5v0m",
    "include_groups" : "album",
    "market" : "CA",
    "limit" : 50,
    "offset" : 0,
}

#send get request
try:
    response = requests.get(artist_url, headers = artist_header, params = album_params)

    response.raise_for_status()
    print(f"Artist Albums Request: {response.status_code}")
except requests.exceptions.HTTPError as http_error:
    print(f"Artist Albums Request HTTP Error: {http_error}")
except requests.exceptions.RequestException as error:
    print(f"Artist Albums Request Other Error: {error}")

# convert to dictionary and use items key to get artist album data
artist_albums = response.json()["items"]
# print album and releast date
for album in artist_albums:
    album_name = album["name"]
    album_release = album["release_date"]
    print(f"{album_name}: {album_release}")

