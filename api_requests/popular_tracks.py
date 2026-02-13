from api_requests import access_api
import base64
import json
import requests 

#get top tracks
def top_tracks(token, artist_uri):
    track_url =f"https://api.spotify.com/v1/artists/{artist_uri}/top-tracks"
    artist_header = {
        "Authorization": f"Bearer {token}"
    }

    track_params = {
        "id": artist_uri,
        "market" : "CA"
    }
    try:
        response = requests.get(track_url, headers = artist_header, params = track_params)

        response.raise_for_status()
        print(f"Top Tracks Request: {response.status_code}")
    except requests.exceptions.HTTPError as http_error:
        print(f"Top Tracks Request HTTP Error: {http_error}")
    except requests.exceptions.RequestException as error:
        print(f"Top Tracks Request Other Error: {error}")

    artist_tracks = response.json()["tracks"]

    return artist_tracks

    