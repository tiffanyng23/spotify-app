from dash import Dash, dash_table, html, dcc, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
from api_requests.access_api import get_token
from api_requests.artist_albums import albums, album_popularity_length
from api_requests.popular_tracks import top_tracks
from api_requests.search_artist import search
from api_requests.all_tracks import all_tracks, all_track_uris, chunk_list, tracks_popularity
from PIL import Image
import urllib.request
import pandas as pd
import time
import re

#create app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

#app layout
app.layout = dbc.Container([
    dcc.Store(
        id="artist-data"
    ),
    html.H1(children="A Reimagined Spotify Artist Explore Page"),
    html.Div(children=" Want to explore music of a new artist but don't know where to start? Type in the artist's name, click submit, and get exploring!"),

    html.Div([dcc.Input(id="artist-input", type="text", value="frank ocean", placeholder="Input Artist Name"),
    html.Button("Submit", id="submit-button", n_clicks=0)]),
    html.Br(),
    dbc.Row(
            dcc.Tabs(id="artist-tabs", value="tab-1", children=[
            dcc.Tab(label="Albums", value="tab-1", children=[
                    dash_table.DataTable(
                        id = "album-table",
                        filter_action="native",
                        filter_options={"placeholder_text": "Filter column..."},
                        sort_action="native",
                        sort_mode="single",
                        row_deletable=False,
                        page_action="native",
                        page_current= 0,
                        page_size=10,
                    )
                ]),
            dcc.Tab(label="Top Tracks", value="tab-2", children=[
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.P("Order By:"),
                                dcc.RadioItems(id="order-radio", options=["Least to Most Popular", "Most to Least Popular"], value= "Most to Least Popular", inline=True),
                                ]),
                            ], width=6),
                        dbc.Col([
                            html.Div([
                                html.P("Select Number of Tracks to Display:"),
                                dcc.RadioItems(id="tracks-radio", options = ['10', '20', '30', '50', 'All'], value = '20', inline=True),
                            ]),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="tracks-bar")
                    ]),
                ]),
            dcc.Tab(label="Still not sure where to start?", value="tab-3", children=[
                    html.Div(id="top-tracks"),
                ])
            ]), 
        )
    ], fluid=False)


# callbacks 
# gather all api data 
@callback(
    Output("artist-data", "data"),
    Input("submit-button", "n_clicks"),
    State("artist-input", "value"),
    prevent_initial_call=True
)
def fetch_data(n_clicks, artist):
    #get authorization token
    token = get_token()
    #get artist uri
    uri = search(token, artist)
    #get all album data from artist uri
    albums_data = albums(token, uri)
    #get album popularity
    album_pop_length = album_popularity_length(token, albums_data)
    #get top tracks from artist
    top = top_tracks(token, uri)
    #get all tracks from an albums json data
    tracks = all_tracks(token, albums_data)
    #get all track ids a list of tracks
    track_ids = all_track_uris(tracks)
    #get data grame of track name : popularity score
    tracks_df = tracks_popularity(token, track_ids)

    return {
        "albums": albums_data,
        "album_popularity_length": album_pop_length,
        "top_tracks": top,
        "tracks_df": tracks_df.to_dict("records")
    }


#album table
@callback(
    Output("album-table", "data"),
    Output("album-table", "columns"),
    Input("artist-data", "data")
)
def album_info(data):
    '''user types in artist --> search for artist --> get uri --> get album data to create a table'''
    if not data:
        return no_update

    # table columns: album name, release date, popularity, and link to listen
    # key would be album uri, values would be each of the columns
    table_data = []
    #extract popularity scores
    popularity_length = data["album_popularity_length"] #stores in dictionary - album uri:[score, length]

    for album_item in data["albums"]:
        #get album uri key to extract popularity value
        pattern = r"spotify:album:"
        uri_string = album_item["uri"]
        uri = re.sub(pattern, "", uri_string)

        #fill table data
        table_data.append(
            {"Popularity": popularity_length[uri][0], #use album uri to get score for specific album
            "Number of Tracks": popularity_length[uri][1],
            "Name": album_item["name"], 
            "Release Date": album_item["release_date"],
            "Album Link": f"[Listen]({album_item['external_urls']['spotify']})"} #markdown format for link
        )

    #columns - id must match key values since it's used to populate the table
    #name is what is displayed on the table and can be anything
    columns = [
        {"name": "Album Name", "id": "Name"},
        {"name": "Release Date", "id": "Release Date"},
        {"name": "Popularity", "id": "Popularity"},
        {"name": "Number of Tracks", "id": "Number of Tracks"},
        {"name": "Album Link", "id":"Album Link", "presentation":"markdown"},
        ]
    return table_data, columns
        
        

#top tracks
@callback(
    Output("top-tracks", "children"),
    Input("artist-data", "data")
)
def render_top_tracks(data):
    '''user types in artist --> search for artist --> get uri --> get top 10 most popular tracks'''
    if not data:
        return no_update
    #return list of top tracks
    t = [html.Li(track["name"]) for track in data["top_tracks"]]
    return html.Ul(t)


# gather popularity value for all album tracks
@callback(
    Output("tracks-bar", "figure"),
    Input("artist-data", "data"),
    Input("tracks-radio", "value"),
    Input("order-radio", "value"),
)
def tracks_graph(data, number_tracks, order):
    if not data:
        return no_update

    #get tracks, popularity data frame
    df = pd.DataFrame(data["tracks_df"])

    #sort tracks by requested order
    if order == "Least to Most Popular":
        sorted_df = df.sort_values(by="popularity")
    else:
        sorted_df = df.sort_values(by="popularity", ascending=False)

    #display requested number of tracks
    if number_tracks == "All":
        filtered_df = sorted_df
    else:
        filtered_df = sorted_df.head(int(number_tracks))

    #create scatter graph 
    fig = px.bar(
        filtered_df,
        x="track",
        y="popularity",
        hover_data=["track", "popularity"],
        orientation="v",
    )
    fig.update_xaxes(showticklabels=False)

    return fig

#run app
if __name__ == '__main__':
    app.run(debug=True)


