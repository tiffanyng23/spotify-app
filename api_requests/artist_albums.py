from api_requests import access_api
import base64
import json
import re
import requests 
import time


#request artist albums data
def albums(token, artist_uri):
    """ search for albums of a specified artist """

    album_url =f"https://api.spotify.com/v1/artists/{artist_uri}/albums"
    header = {
        "Authorization": f"Bearer {token}"
    }
    # query string used for requests.get
    album_params = {
        "id": artist_uri,
        "include_groups" :["album"],
        "market" : "CA",
        "limit" : 50,
        "offset" : 0,
    }

    #send get request
    try:
        response = requests.get(album_url, headers = header, params = album_params)

        response.raise_for_status()
        print(f"Artist Albums Request: {response.status_code}")
    except requests.exceptions.HTTPError as http_error:
        print(f"Artist Albums Request HTTP Error: {http_error}")
    except requests.exceptions.RequestException as error:
        print(f"Artist Albums Request Other Error: {error}")

    # convert to dictionary and use items key to get artist album data
    albums_data = response.json()["items"]
    return albums_data

def album_popularity_length(token, albums_data):
    '''get list of popularity scores of each of an artists albums'''
    #list of album popularity 
    albums_pop_length = {}

    #use regex to isolate album uri from album data set
    for one_album in albums_data:
        pattern = r"spotify:album:"
        uri_string = one_album["uri"]
        uri = re.sub(pattern, "", uri_string)
            
        album_url =f"https://api.spotify.com/v1/albums/{uri}/"
        header = {
            "Authorization": f"Bearer {token}"
        }
        # query string used for requests.get
        album_params = {
            "market" : "CA",
        }
        #send get request to get album specific data
        try:
            response = requests.get(album_url, headers = header, params = album_params)

            response.raise_for_status()
            print(f"Album Request: {response.status_code}")
            # convert to dictionary and extract album popularity
            #album uri is key, value is pop score and total number of tracks
            albums_pop_length[uri] = [response.json()["popularity"], response.json()["total_tracks"]]
        except requests.exceptions.HTTPError as http_error:
            print(f"Album Request HTTP Error: {http_error}")
        except requests.exceptions.RequestException as error:
            print(f"Album Request Other Error: {error}")
    
    return albums_pop_length

    

