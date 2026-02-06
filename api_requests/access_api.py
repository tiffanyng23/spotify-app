import requests 
import base64
import json

#api request
# client id and client secrete extracted upon web app creation
client_id = "48584cf868a64fab9cdcdf344e8b3b75"
client_secret = "b25232e937314ca18c64b2e1e26cd8f6"
auth_str = f"{client_id}:{client_secret}"
b64_auth = base64.b64encode(auth_str.encode()).decode()
url = "https://accounts.spotify.com/api/token"

headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/x-www-form-urlencoded" # tells server how to interpret payload data
}

data = {
    "grant_type": "client_credentials"
}

# post request 
try:
    # send post request with data to get access token
    response = requests.post(url, headers=headers, data=data)

    # check if response has 4xx or 5xx status code
    response.raise_for_status()
    print(f"Token Request: {response.status_code}")
except requests.exceptions.HTTPError as http_error:
    print(f"HTTP error occured: {http_error}")
except requests.exceptions.RequestException as error:
    print(f"Other error: {error}")

# get access token
token = response.json().get("access_token")