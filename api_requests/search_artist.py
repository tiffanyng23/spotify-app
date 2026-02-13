from api_requests import access_api
import base64
import json
import re
import requests 

#request artist albums data
def search(token, artist):
    """ search for artist to get spotify id of artist """

    search_url =f"https://api.spotify.com/v1/search"
    header = {
        "Authorization": f"Bearer {token}" # get token from access_api module
    }
    # query string used for requests.get
    search_params = {
        "q": artist, #query is artist user wants to search
        "type": "artist",
        "market" : "CA",
        "limit" : 50,
        "offset" : 0,
    }

    #send get request
    try:
        response = requests.get(search_url, headers = header, params = search_params)

        response.raise_for_status()
        print(f"Search Artist Request: {response.status_code}")
    except requests.exceptions.HTTPError as http_error:
        print(f"Search Artist Request HTTP Error: {http_error}")
    except requests.exceptions.RequestException as error:
        print(f"Search Artist Request Other Error: {error}")

    # convert to dictionary and use items key to get search data
    #extracts value of uri
    artist_search = response.json()["artists"]["items"][0]["uri"]

    #use regex to isolate uri 
    pattern = r"spotify:artist:"
    uri = re.sub(pattern, "", artist_search)
    return uri
