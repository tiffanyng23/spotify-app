from dash import Dash, dash_table, html, dcc, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import random
import re
import time
from api_requests.access_api import get_token
from api_requests.all_tracks import all_tracks, all_track_uris, chunk_list, tracks_popularity
from api_requests.artist_albums import albums, album_popularity_length
from api_requests.popular_tracks import top_tracks
from api_requests.search_artist import search


#create app
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server

#app layout
app.layout = dbc.Container([
    dcc.Store(
        id="artist-data"
    ),
    html.H1(children="Spotify Artist Page: Reimagined"),
    html.Div([
            dcc.Input(id="artist-input", type="text", value="", placeholder="Input Artist Name"),
            html.Button("Submit", id="submit-button", n_clicks=0, disabled=True)
        ], style={"display": "flex", "justifyContent": "center"}
    ),
    html.Br(),
    dbc.Row(
            dcc.Tabs(id="artist-tabs", value="tab-1", children=[
            dcc.Tab(label="Albums", className="album-table", value="tab-1", children=[
                    html.Br(),
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
                        style_filter_conditional=[{
                                "if": {"column_editable": False},
                                "backgroundColor": "rgba(127, 75, 196, 0.6)",
                                "border": "1px solid rgba(255, 255, 255, 1)"
                            }],
                        style_data_conditional=[{
                                "if": {"state": "active"},
                                "backgroundColor": "rgba(30,215,96,0.8)",
                                "border": "1px solid rgba(255, 255, 255, 1)"
                            }],
                        ),
                ]),
            dcc.Tab(label="Album Tracks", value="tab-2", children=[
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Most Mainstream Album Tracks"),
                                    html.P("(Highest Spotify Popularity Value)"),
                                    html.Ul(id="popular-tracks"),
                                ])
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Tracks Based on Mainstream vs. Hipster Level"),
                                    html.Br(),
                                    html.Label("Hipster vs. Mainstream"),
                                    dcc.Slider(
                                        min = 0, 
                                        max = 100, 
                                        step =1,
                                        id="popular-hipster-slider",
                                        marks={
                                            "0": {"label": "Hipster", "style": {"color": "rgb(255,255,255)", "fontSize": "9px"}},
                                            "100": {"label": "Mainstream", "style": {"color": "rgb(255,255,255)", "fontSize": "9px"}},
                                        },
                                        allow_direct_input=False,
                                        value=50),
                                    html.Ul(id="custom-tracks-list"),
                                ])
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Most Hipster Album Tracks"),
                                    html.P("(Lowest Spotify Popularity Value)"),
                                    html.Ul(id="hipster-tracks")
                                ])
                            ),
                        )
                    ],),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Order By: "),
                            dcc.RadioItems(id="order-graph", options=["Most Hipster", "Most Mainstream"], value= "Most Mainstream", labelStyle={"margin-right": "20px"}, inline=True),
                        ], md=4),
                        dbc.Col([
                            html.Label("Percentage of Total Tracks to Display: "),
                            dcc.Slider(
                                0, 
                                100, 
                                5, 
                                marks={
                                    "0": {"label": "0", "style": {"color": "rgb(255,255,255)"}},
                                    "10": {"label": "10", "style": {"color": "rgb(255,255,255)"}},
                                    "20": {"label": "20", "style": {"color": "rgb(255,255,255)"}},
                                    "30": {"label": "30", "style": {"color": "rgb(255,255,255)"}},
                                    "40": {"label": "40", "style": {"color": "rgb(255,255,255)"}},
                                    "50": {"label": "50", "style": {"color": "rgb(255,255,255)"}},
                                    "60": {"label": "60", "style": {"color": "rgb(255,255,255)"}},
                                    "70": {"label": "70", "style": {"color": "rgb(255,255,255)"}},
                                    "80": {"label": "80", "style": {"color": "rgb(255,255,255)"}},
                                    "90": {"label": "90", "style": {"color": "rgb(255,255,255)"}},
                                    "100": {"label": "100", "style": {"color": "rgb(255,255,255)"}},
                                },
                                id="tracks-graph", 
                                allow_direct_input=False,
                                tooltip={"style": {"color": "rgb(0,0,0)", "fontSize": "12px"}},
                                value = 20),
                        ], md=4),
                    ]),
                    dbc.Row([
                        dcc.Graph(id="tracks-bar"),
                    ]),
                ]),
            dcc.Tab(label="Still Not Sure Where to Start?", value="tab-3", children=[
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                             dbc.Card(
                                dbc.CardBody([
                                    html.H4("Spotify Generated Top Tracks"),
                                    html.P("Similar to the Most Popular Tracks list but includes non-album tracks and tracks the artist contributed to as a feature."),
                                    html.P(id="top-tracks"),
                                    html.Br(),
                                    html.H4("Random Album Generator"),
                                    html.Button("Click for a Random Album", id="random-album", n_clicks=0, disabled=True),
                                    html.Br(),
                                    html.H4("Random Track Generator"),
                                    html.Button("Click for a Random Track", id="random-track", n_clicks=0, disabled=True),
                                ])
                            ),
                        ], md=6),
                    ], justify="center")
                ])
            ]) 
        ),
        html.Img(
            id="spotify-logo",
            src='assets/Full_Logo_Green_RGB.svg',
            alt='spotify_logo'
        )
    ], fluid=False)


# callbacks 
#ensure input button can only be clicked if there is content
@callback(
    Output("submit-button", "disabled"),
    Output("random-album", "disabled"),
    Output("random-track", "disabled"),
    Input("artist-input", "value")
)
def set_button_state(artist_name):
    if not artist_name:
        return True, True, True
    else:
        return False, False, False


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
    if not uri: #if the artist cannot be found
        return no_update
    #get all album data from artist uri
    albums_data = albums(token, uri)
    if not albums_data: #if the artist has no albums
        return no_update
    #get album popularity
    album_pop_length = album_popularity_length(token, albums_data)
    #get top tracks from artist
    top = top_tracks(token, uri)
    #get all tracks from an albums json data
    tracks = all_tracks(token, albums_data)
    #get all track ids a list of tracks
    track_ids = all_track_uris(tracks)
    #get data frame of track name : popularity score
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
            "Album Link": f"[LISTEN ON SPOTIFY]({album_item['external_urls']['spotify']})"} #markdown format for link
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
        
    

# Most popular, most hipster tracks
@callback(
    Output("popular-tracks", "children"),
    Output("hipster-tracks", "children"),
    Input("artist-data", "data"),
)
def track_lists(data):
    if not data:
        return no_update
    #get all the tracks, convert to a dataframe and sort by popularity in descending order 
    df = pd.DataFrame(data["tracks_df"]).sort_values("popularity", ascending=False)

    #gather popular (most popular) and hipster (least popular) tracks
    popular_df = df[["track", "popularity", "url"]].head(10)
    hipster_df = df[["track", "popularity", "url"]].tail(10)
    popular_tracks = [html.Li(html.A(track[0], href=track[2], target="_blank")) for track in popular_df.itertuples(index=False)]
    hipster_tracks = [html.Li(html.A(track[0], href=track[2], target="_blank")) for track in hipster_df.itertuples(index=False)]

    return html.Ul(popular_tracks), html.Ul(hipster_tracks)

# custom list tracks
@callback(
    Output("custom-tracks-list", "children"),
    Input("artist-data", "data"),
    Input("popular-hipster-slider", "value"),
)
def track_lists(data, custom_slider):
    if not data:
        return no_update

    #get all the tracks, convert to a dataframe and sort by popularity 
    df = pd.DataFrame(data["tracks_df"]).sort_values("popularity", ascending=False) #want most popular at top of list
    
    #find row that fits in this percentage (e.g. 80% mainstream), so we want the tracks closest to the top 20% of list
    top_percent = float((100-custom_slider)/100)
    row = int(len(df)* top_percent)

    #gather track in that row along with 2 above and 2 below to get 5 tracks 
    #for 100% 
    if top_percent == 0:
        custom_df = df[["track", "popularity", "url"]].iloc[0:5]
    #for 0%
    elif top_percent == 1:
        custom_df = df[["track", "popularity", "url"]].iloc[-5:] # bottom 5 rows
    else:
        row_index = row - 1
        custom_df = df[["track", "popularity", "url"]].iloc[row_index-2:row_index+3]
    
    track_list = [html.Li(html.A(row[0], href=row[2], target="_blank")) for row in custom_df.itertuples(index=False)]
    return html.Ul(track_list)


# gather popularity value for all album tracks
@callback(
    Output("tracks-bar", "figure"),
    Input("artist-data", "data"),
    Input("order-graph", "value"),
    Input("tracks-graph", "value"),
)
def tracks_graph(data, order, percent_of_tracks):
    if not data:
        return no_update

    #get tracks, popularity data frame
    df = pd.DataFrame(data["tracks_df"])

    #sort tracks by requested order
    if order == "Most Hipster":
        sorted_df = df.sort_values(by="popularity", ascending=True)
    else:
        sorted_df = df.sort_values(by="popularity", ascending=False)
    
    # find number of tracks to display
    number_tracks = len(sorted_df)*(float(percent_of_tracks)/100)

    #display requested number of tracks
    filtered_df = sorted_df.head(int(number_tracks))

    #create scatter graph 
    fig = px.bar(
        filtered_df,
        x="uri",
        y="popularity",
        custom_data=["track", "popularity", "album"],
        orientation="v",
    )
    fig.update_traces(
        marker_color="rgb(30,215,96)",
        hovertemplate=
            "Track: %{customdata[0]}<br>" +
            "Popularity: %{customdata[1]}<br>" +
            "Album: %{customdata[2]}<extra></extra>")
    fig.update_yaxes(title= "Popularity", title_font={"color": "rgb(255,255,255)"}, tickfont={"color": "rgb(255,255,255)"})
    fig.update_xaxes(title= "Tracks", title_font={"color": "rgb(255,255,255)"}, showticklabels=False, )
    fig.update_layout(
        title="Popularity Value of Album Tracks <br><sup>Note: There are some tracks that appear in multiple albums which are displayed in separate bars. Hover over the bar to view the popularity of the track based on album.</sup>",
        font_color="rgb(255,255,255)",
        paper_bgcolor="rgb(68,68,68)"
    )

    return fig

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
    t = [html.Li(html.A(track["name"], href=track["external_urls"]["spotify"], target = "_blank")) for track in data["top_tracks"]]
    return html.Ul(t)

#random album and track generator
@callback(
    Output("random-album", "children"),
    Output("random-track", "children"),
    Input("artist-data", "data"),
    Input("random-album", "n_clicks"),
    Input("random-track", "n_clicks"),
)
def random_choice_generator(data, album_click, track_click):
    if not data:
        return no_update
    # random album
    album_urls = []
    for album in data["albums"]:
        album_urls.append(album["external_urls"]["spotify"])
    album_link = random.choice(album_urls)

    #random track
    track_urls =[]
    #go through each row and extract the track url
    for track in data["tracks_df"]:
        track_urls.append(track["url"])
    track_link = random.choice(track_urls)
    # returns random album and track link
    return html.A("CLICK FOR A RANDOM ALBUM", href=album_link, target="_blank"), html.A("CLICK FOR A RANDOM TRACK", href=track_link, target="_blank")

#run app
if __name__ == '__main__':
    app.run(debug=True)


