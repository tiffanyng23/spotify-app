# spotify-app
A reimagined Spotify Artist Explore Page where you can search album and track information for any artist on Spotify.


## Why did I make this page?
Sometimes I find that I don't know where to start when wanting to explore the music catalogue of a new artist. The artist's page on Spotify begins with a list of 10 of their current most popular tracks, and is followed by a list of their discography and some playlists they are featured in. I find at first glance, it can be difficult to know where to start, especially if they have a lot of tracks and albums!. 

I created a reimagined Spotify Artist Explore Page to helps users decide where to start when exploring a new artist. It has a lot of the same components seen on Spotify, but focuses more on exploring artist albums and tracks that are from albums (doesn't really focus on tracks the artist is featured in). I wanted this page to be more album-centric, since I feel albums show more of the artists artistic and musical vision. Personally, I prefer listening to albums over playlists since I like exploring overarching themes, transitions, and sounds across tracks in an album. This reflects how I approached the layout and focus of this page. 

The criteria used to organize these songs and tracks is somewhat based on Spotify's popularity score which is defined on the Spotify Web API page as: 

"The value will be between 0 and 100, with 100 being the most popular. The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are. Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity. Note: the popularity value may lag actual popularity by a few days: the value is not updated in real time."

Using the popularity value as a factor for which tracks (and albums) to display is a method that is not tailored to the specific user, but moreso a way to introduce the user to tracks (and albums) from an artist that are considered fan favourites. This is a good way to gain an introduction to elements of an artist's music that appeals to their fans. If users want to explore an artists less popular work, this can be done by listening to the tracks and albums with a lower popularity value. 


## Components of this Project
There are 3 tabs: "Albums", "Top Tracks", and "Still not sure what to pick?". 

### Albums Tab
The first tab "Albums" contains a table where you can sort all the artists albums based on "popularity", album length, and release date. This allows users to find an album that aligns with how they want to explore an artists music (unfortunately I can no longer access genre information for an album, that would have been great to add). For example, if they want to check out their most popular album, or their newest album. Or if they want to check out their earlier work first, or are looking for a shorter album to get a quick glimpse of the artist. At the right end of the table, there is a column which provides links at which the user can click to listen to their album of choice on Spotify.

### Album Tracks Tab
The second tab "Tracks" is ideal for those who are not as much album listeners, but more tracks and playlist listeners. The top half of this tab has 3 main sections. The left side lists the artists top 5 most "hyped" tracks while the right side lists the artists top 5 most "hipster" tracks. This is determined by the popularity score, where the songs with the top 10 highest score is in the "hyped" tracks list, while the top 10 lowest popularity score is in the "hipster" tracks list. In the middle, there is a customizable list where the user can select the percentage of hyped or hipster tracks they desire. For example, a user may want to get a list of songs that are 60% hyped (i.e. top 40% popularity value), or 90% hipster (i.e. bottom 10% popularity value). The tracks in these 3 lists are all hyperlinked, allowing users to easily listen to the track they desire. At the bottom of this tab there is a customizable bar chart which shows the popularity score of the artists album tracks. Users can filter tracks included based on order (Most Hyped or Most Hipster) and number of tracks to display.

### Not Sure What to Pick?
This tab is for users who truly want to randomnly select a track to listen to. On the left side, there is a list of the artist's Spotify top tracks. This matches up with the 10 tracks shown on the top of an artists page on Spotify. It likely differs a bit from the "hyped" tracks list in the Album Tracks Tab since it also considers non-album tracks. On the right side, there is a random song generator. For those who really cannot decide on what to listen to, by clicking the button, it will randomnly select one of the artist's tracks and open the link for the user. 
