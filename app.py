from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from api_requests import access_api, artist_albums, artist_tracks

#create app
app = Dash(__name__)
server = app.server

#app layout
app.layout = [
    html.H1(children='Spotify Artist Summary', style={'textAlign':'center'}),
]

# search for artist

#customizable summary dashboard 
# number of albums, newest album (link to album), number of tracks, newest track (link to track)
# average length of album, year 

#3 columns: album/tracks/artists images should be linked to respective spotify pages
#left - artist albums
#centre - artist top tracks
#right recommended artists 

#download feature
#be able to download the summary dashboard


#callbacks

#run app
if __name__ == '__main__':
    app.run(debug=True)
