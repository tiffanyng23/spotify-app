from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
from api_requests.access_api import get_token
from api_requests.artist_albums import albums
from api_requests.artist_tracks import top_tracks
from api_requests.search_artist import search
from api_requests.recommended_artists import artist_recs
from PIL import Image
import urllib.request

#create app
app = Dash(__name__)
server = app.server

#app layout
app.layout = dbc.Container([
    html.H1(children='Spotify Comprehensive Artist Page'),
    html.Div(children=" An application where you can gather album and track information for your favourite artists."),

    html.Div([dcc.Input(id="artist-input", type="text", value="beyonce", placeholder="Input Artist Name"),
    html.Button("Submit", id="submit-button", n_clicks=0)]),
    dbc.Row(
            dcc.Tabs(id="artist-tabs", value="tab-1", children=[
            dcc.Tab(label="Albums", value="tab-1", children=[
                    html.Div(id="album-covers")
                ]),
            dcc.Tab(label="Top Tracks", value="tab-2", children=[
                    html.Div(id="top-tracks")
                ])
            ]), 
        )
    ], fluid=False)

# callbacks 
# album images

#album covers
@callback(
    Output("album-covers", "children"),
    Input("artist-tabs", "value"),
    Input("submit-button", "n_clicks"), #callback triggered upon clicking submit
    State("artist-input", "value"), #state provides data without triggering the callback 
    prevent_initial_call=True
)
def artist_uri(tab, n_clicks, artist):
    '''user types in artist --> search for artist --> get uri --> get album cover/info'''
    #api request
    token = get_token()
    #get artist uri
    uri = search(token, artist)

    #get albums
    artist_albums = albums(token, uri)
    # get album image, store as list of images
    album_covers=[]
    for album in artist_albums:
        if album.get("images"):
            album_covers.append(
                    html.Img(src = album["images"][0]["url"], #get image url 
                    style={"width": "150px", "height": "150px"})
                )
    return album_covers # images take up half of page

#top tracks
@callback(
    Output("top-tracks", "children"),
    Input("artist-tabs", "value"),
    Input("submit-button", "n_clicks"), #callback triggered upon clicking submit
    State("artist-input", "value"), #state provides data without triggering the callback 
    prevent_initial_call=True
)
def artist_uri(tab, n_clicks, artist):
    '''user types in artist --> search for artist --> get uri --> get top 10 most popular tracks'''
    #api request
    token = get_token()
    #get artist uri
    uri = search(token, artist)

    # get top tracks
    tracks = top_tracks(token, uri)
    t = [html.Li(track["name"]) for track in tracks]
    return html.Ul(t)


# highlight bottom 10 tracks based on popularity - hipster vibes

#run app
if __name__ == '__main__':
    app.run(debug=True)


