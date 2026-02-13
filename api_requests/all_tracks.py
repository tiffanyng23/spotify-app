import requests 
import base64
import json
import re
from api_requests import access_api
import pandas as pd
import time

def all_tracks(token, albums_data):
    '''Use album dataset (contains all of the artists data) to extract each albums uri, returns all the albums tracks'''
    
    #extract uri for each of the artists albums
    all_album_tracks = []
    # loop through each album to get all the tracks in each album
    for album in albums_data:
        #use regex to isolate album uri from album data set
        pattern = r"spotify:album:"
        uri_string = album["uri"]
        uri = re.sub(pattern, "", uri_string)


        album_url = f"https://api.spotify.com/v1/albums/{uri}/tracks" 

        header = {
                "Authorization": f"Bearer {token}"
            }

        album_params = {
            "market" : "CA",
            "limit" : 50,
            "offset" : 0,
        }

        #send get request to gather all album tracks
        try:
            response = requests.get(album_url, headers = header, params=album_params)
            response.raise_for_status()

            #convert to json
            album_tracks_data = response.json()["items"]
            # add each albums tracks to the all albums tracks list
            all_album_tracks.append(album_tracks_data)
            print(f"Album's Tracks Request: {response.status_code}")
        except requests.exceptions.HTTPError as http_error:
            print(f"Album's Tracks Request HTTP Error: {http_error}")
        except requests.exceptions.RequestException as error:
            print(f"Album's Tracks Request Other Error: {error}")
        
        #let spotify rest for 200ms after gathering the tracks data for each album before another request
        time.sleep(0.2)

    return all_album_tracks

def all_track_uris(all_album_tracks):
    '''Provide all album tracks to get each albums tracks uri, returns a unique list of the id's'''
    #get track uri's for the album and store in dictionary
    track_popularity={}

    #store all track id's 
    track_ids=[]
    # go through each album
    for album in all_album_tracks:
        #go through each track in each album
        for track in album:
            #extract the track's uri
            uri = track["uri"]
            #add track uri to list holding all track uri's
            track_ids.append(track["id"])
    track_ids = list(set(track_ids))

    return track_ids

#create batches of track uri's to allow for batch api requests
def chunk_list(lst, size=50):
    '''helper function that takes list of track uri's and splits it into chunks of 50'''
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def tracks_popularity(token, track_ids):
    '''do api requests for chunks of track_ids and determine popularity score'''
    # create dictionary to hold track name and its popularity score
    track_popularity={}

    for batch in chunk_list(track_ids, 50):
    #api request for track 
    #same header as for the earlier request above, different params
        tracks_url = f"https://api.spotify.com/v1/tracks" 
        header = {
                "Authorization": f"Bearer {token}"
            }
        track_params = {
                "ids" : ",".join(batch),
                "market" : "CA",
            }
        try:
            response = requests.get(tracks_url, headers=header, params=track_params)
            response.raise_for_status()
            print(f"Track Data Request: {response.status_code}")
            #convert data to json and extract info store in dictionary
            #get requests for multiple tracks has the tracks stored as a value like "tracks": [{},{}...]
            for track in response.json()["tracks"]:
                #extract url
                track_url = track["external_urls"]["spotify"]

                #add each track to the dictionary
                track_popularity[track["uri"]] = {"track" :track["name"], "popularity":track["popularity"], "url": track_url}
        except requests.exceptions.HTTPError as http_error:
            print(f"Track Data Request HTTP Error: {http_error}")
        except requests.exceptions.RequestException as error:
            print(f"Track Data Request Other Error: {error}")
        
        # rest before next api request
        time.sleep(0.2)  # wait 200ms before next batch

    #convert dictionary to dataframe to allow for smoother graphing
    #track, popularity, url represents the columns, sort in descending order by default
    track_pop_df = (pd.DataFrame.from_dict(track_popularity, columns=["uri", "track", "popularity", "url"], orient="index"))
    #make sure all popularity values are numbers and not strings
    track_pop_df["popularity"] = pd.to_numeric(track_pop_df["popularity"], errors="coerce")
    track_pop_df = track_pop_df.sort_values(by="popularity", ascending=False)

    return track_pop_df
